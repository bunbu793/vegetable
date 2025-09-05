import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import json
from datetime import datetime
from modules.titles import 称号データ, get_title_info, check_titles
from modules.mission import generate_mission, RECIPE_DB, HIDDEN_VEGETABLES
import time 
from collections import defaultdict

# ------------------------
# ゾンビ度の理由説明
# ------------------------
def explain_zombie_reason(score):
    if score < 30:
        return "画像のほとんどが明るく鮮やかで、腐敗の兆候は見られませんでした。"
    elif score < 60:
        return "一部に暗くくすんだ領域があり、腐敗が始まりつつあると判断されました。"
    elif score < 80:
        return "画像の多くに暗さと低彩度が見られ、腐敗が進行している状態です。"
    else:
        return "画像全体が暗く、色も失われており、完全にゾンビ化していると判定されました。"

# ------------------------
# ページ設定
# ------------------------
st.set_page_config(page_title="野菜ゾンビ診断", page_icon="🧟‍♂️")
st.title("🧟‍♂️ 野菜ゾンビ度診断アプリ")
st.write("まずはルール説明を読もう！左上の ≫ マークから「Rules」を選んでね！")

# ------------------------
# ログインフォーム
# ------------------------
with st.form("login_form"):
    username = st.text_input("ユーザー名を入力してください")
    password = st.text_input("パスワードを入力してください", type="password")
    submitted = st.form_submit_button("ログイン")

if submitted:
    profile_path = f"user_profiles/{username}.json"
    if os.path.exists(profile_path):
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
        if profile.get("password") == password:
            st.success("🔓 ログイン成功！")
            st.session_state.update({
                "authenticated": True,
                "username": username,
                "titles": profile.get("titles", []),
                "missions_completed": profile.get("missions_completed", []),
                "points": profile.get("points", 0),
                "items_owned": profile.get("items_owned", [])
            })
        else:
            st.error("❌ パスワードが間違っています")
    else:
        st.info("🆕 新規ユーザーとして登録されます")
        st.session_state.update({
            "authenticated": True,
            "username": username,
            "titles": [],
            "missions_completed": [],
            "points": 0,
            "items_owned": []
        })

# ------------------------
# 認証後の処理
# ------------------------
if st.session_state.get("authenticated"):
    st.header(f"ようこそ、{st.session_state['username']} さん！")
    st.metric("所持ポイント", f"{st.session_state['points']} pt")

    # 画像取得
    input_method = st.radio("写真の取得方法を選んでください", ["カメラで撮影", "ファイルをアップロード"])
    image_bytes = st.camera_input("野菜の写真を撮ってください") if input_method == "カメラで撮影" else \
                  st.file_uploader("野菜の写真をアップロードしてください", type=["png", "jpg", "jpeg"])

    # ゾンビ度計算関数
    def calculate_zombie_score(image_bytes):
        img = Image.open(image_bytes)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
        low_saturation = cv2.inRange(hsv, (0, 0, 0), (180, 50, 255))
        zombie_ratio = np.sum(low_saturation > 0) / low_saturation.size
        return round(zombie_ratio * 100, 1)

    if image_bytes:
        score = calculate_zombie_score(image_bytes)

        # 腐敗防止スプレー使用
        if "腐敗防止スプレー" in st.session_state["items_owned"]:
            if st.button("🧪 腐敗防止スプレーを使う"):
                score = max(score - 10, 0)
                st.success("腐敗防止スプレーを使用！ゾンビ度が10%下がりました")
                st.session_state["items_owned"].remove("腐敗防止スプレー")

        # 診断結果表示
        st.image(image_bytes, caption="診断対象の野菜", use_container_width=True)
        st.progress(score / 100)
        st.metric("ゾンビ度", f"{score}%")
        with st.expander("診断の理由を見る"):
            st.markdown(f"🧠 理由：{explain_zombie_reason(score)}")

        # コメント
        if score < 30:
            st.success("✅ フレッシュ！ゾンビの気配なし。")
            st.markdown("🥦「まだ元気だよ！早く食べてね！」")
        elif score < 60:
            st.warning("⚠️ ややゾンビ化。早めに調理しましょう。")
            st.markdown("🍅「ちょっと疲れてきたかも…」")
        elif score < 80:
            st.error("🚨 ゾンビ化進行中！今すぐ炒めて！")
            st.markdown("🥕「うぅ…腐りかけてる…」")
        else:
            st.error("🧟‍♂️ 完全にゾンビ化！冷蔵庫から避難してください！")
            st.markdown("🧟‍♂️「助けて…もう腐っちゃう…」")

        # 野菜選択肢（隠し野菜含む）
        available_veggies = list(RECIPE_DB.keys())
        for hidden_veg, data in HIDDEN_VEGETABLES.items():
            if data["解放条件"] in st.session_state["items_owned"]:
                available_veggies.append(hidden_veg)

        vegetable_name = st.selectbox("撮影した野菜を選んでください", available_veggies)
        mission = generate_mission(vegetable_name, score)
        st.subheader("🎯 今日のミッション")
        st.markdown(mission["mission"])
        st.session_state["current_mission"] = mission

        # ===== rerun 両対応ユーティリティ =====
        def safe_rerun():
            if hasattr(st, "rerun"):
                st.rerun()
            elif hasattr(st, "experimental_rerun"):
                st.experimental_rerun()

        # ===== 自作オートリフレッシュ関数 =====
        def tick_every_second(active_flag_key="mission_active", tick_key="__tick__", interval=1.0):
            if not st.session_state.get(active_flag_key):
                return
            now = time.time()
            last = st.session_state.get(tick_key, 0.0)
            if now - last >= interval:
                st.session_state[tick_key] = now
                safe_rerun()

        # ===== 初期化 =====
        if "mission_active" not in st.session_state:
            st.session_state["mission_active"] = False
        if "points" not in st.session_state:
            st.session_state["points"] = 0

        # ===== モード選択 =====
        mode = st.radio("モードを選んでね", ["制限時間モード", "ストップウォッチモード"])

        # ==============================
        # 制限時間モード
        # ==============================
        if mode == "制限時間モード":
            time_limit_minutes = st.number_input("制限時間（分）", min_value=1, max_value=30, value=5)

            if not st.session_state["mission_active"]:
                if st.button("🚀 ミッション開始！"):
                    st.session_state["mission_start"] = time.time()
                    st.session_state["time_limit"] = time_limit_minutes * 60
                    st.session_state["mission_active"] = True
            else:
                tick_every_second()

                elapsed = time.time() - st.session_state["mission_start"]
                remaining = max(st.session_state["time_limit"] - elapsed, 0)
                minutes = int(remaining // 60)
                seconds = int(remaining % 60)

                if remaining <= 60 and remaining > 0:
                    st.markdown("<style>.stApp {background-color: #ffcccc;}</style>", unsafe_allow_html=True)

                st.metric("残り時間", f"{minutes}分 {seconds}秒")

                if remaining == 0:
                    st.markdown("""
                    <style>
                    @keyframes blink {0%{opacity:1;}50%{opacity:0;}100%{opacity:1;}}
                    .blink {animation: blink 1s infinite; color: red; font-size: 32px; font-weight: bold; text-align: center;}
                    </style>
                    <div class="blink">💀 GAME OVER 💀</div>
                    """, unsafe_allow_html=True)

                if st.button("✅ ミッション達成！"):
                    if remaining > 0:
                        st.success("⏱ 時間内クリア！+10pt")
                        st.session_state["points"] += 10
                        st.balloons()
                    else:
                        st.error("💀 時間切れ！ボーナスなし")
                    st.session_state["mission_active"] = False

        # ==============================
        # ストップウォッチモード
        # ==============================
        elif mode == "ストップウォッチモード":
            if not st.session_state["mission_active"]:
                if st.button("🚀 ミッション開始！"):
                    st.session_state["mission_start"] = time.time()
                    st.session_state["mission_active"] = True
            else:
                tick_every_second()

                elapsed = time.time() - st.session_state["mission_start"]
                minutes = int(elapsed // 60)
                seconds = int(elapsed % 60)
                st.metric("経過時間", f"{minutes}分 {seconds}秒")

                if st.button("✅ ミッション達成！"):
                    elapsed = time.time() - st.session_state["mission_start"]

                    if elapsed <= 60:
                        bonus = 15
                        st.success("🥇 超高速クリア！+15pt")
                        st.balloons()
                    elif elapsed <= 180:
                        bonus = 10
                        st.success("⏱ 早い！+10pt")
                        st.balloons()
                    elif elapsed <= 300:
                        bonus = 5
                        st.info("👍 ナイス！+5pt")
                        st.snow()
                    else:
                        bonus = 2
                        st.warning("お疲れ！+2pt")

                    st.session_state["points"] += bonus
                    st.session_state["mission_active"] = False
                # 証拠画像提出
                proof_method = st.radio("証拠画像の取得方法", ["カメラで撮影", "ファイルをアップロード"])
                proof_image = st.camera_input("証拠写真を撮影してください") if proof_method == "カメラで撮影" else \
                            st.file_uploader("証拠写真をアップロードしてください", type=["png", "jpg", "jpeg"])

                # ミッション達成
                if st.button("✅ ミッション達成！"):
                    mission["timestamp"] = datetime.now().strftime("%Y%m%d%H%M%S")
                    st.session_state["missions_completed"].append(mission)
                    st.session_state["points"] += mission["reward_points"]
                    st.success(f"🎁 報酬ポイント +{mission['reward_points']}pt（合計：{st.session_state['points']}pt）")
                    st.balloons()

            # 証拠画像保存（命名規則統一）
            if proof_image:
                proof_dir = f"user_profiles/{username}_proofs"
                os.makedirs(proof_dir, exist_ok=True)
                proof_path = os.path.join(proof_dir, f"{vegetable_name}_{score}_{mission['timestamp']}.jpg")
                with open(proof_path, "wb") as f:
                    f.write(proof_image.getbuffer())
                st.success("📸 証拠画像を保存しました！")

            # セーブデータ保存
            profile_path = f"user_profiles/{username}.json"
            profile = {
                "username": username,
                "password": password,  # 本番運用ならハッシュ化推奨
                "titles": st.session_state["titles"],
                "missions_completed": st.session_state["missions_completed"],
                "points": st.session_state["points"],
                "items_owned": st.session_state["items_owned"]
            }
            os.makedirs(os.path.dirname(profile_path), exist_ok=True)
            with open(profile_path, "w", encoding="utf-8") as f:
                json.dump(profile, f, ensure_ascii=False, indent=2)
            st.success("💾 セーブデータを保存しました！")
            
            # 称号獲得チェック
            new_titles = check_titles(st.session_state["missions_completed"], st.session_state["titles"])
            for 称号 in new_titles:
                進化元 = None
                for t, data in 称号データ.items():
                    if data.get("進化先") == 称号 and t in st.session_state["titles"]:
                        進化元 = t
                        st.session_state["titles"].remove(t)
                        break

                st.session_state["titles"].append(称号)

                if 進化元:
                    # 🌟 進化演出
                    st.markdown(f"""
                    <div style="text-align:center; font-size:28px; color:gold;">
                    🌟 称号進化！<br><br>
                    <span style="font-size:24px;">{進化元} → <strong>{称号}</strong></span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()

                    # 画像表示（進化前→進化後）
                    old_url = f"https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/{称号データ[進化元]['画像ファイル名']}"
                    new_url = f"https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/{称号データ[称号]['画像ファイル名']}"
                    st.image(old_url, caption=f"旧称号：{進化元}", width=120)
                    st.image(new_url, caption=f"新称号：{称号}", width=150)
                    st.markdown(f"📝 {称号データ[称号]['説明']}")
                else:
                    # 通常の称号獲得演出
                    st.success(f"🏆 称号獲得：{称号}")
                    st.markdown(称号データ[称号]["説明"])
                    image_url = f"https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/{称号データ[称号]['画像ファイル名']}"
                    st.image(image_url, width=150)
                    st.balloons()

            # 過去のミッション履歴表示
            if st.session_state["missions_completed"]:
                st.subheader("📜 過去のミッション達成履歴")
                for i, m in enumerate(st.session_state["missions_completed"], 1):
                    st.markdown(f"{i}. {m['vegetable']} → {m['recipe']}（ゾンビ度：{m['zombie_score']}%）")
                    proof_path = f"user_profiles/{username}_proofs/{m['vegetable']}_{m['zombie_score']}_{m['timestamp']}.jpg"
                    if os.path.exists(proof_path):
                        st.image(proof_path, caption="証拠画像", width=200)