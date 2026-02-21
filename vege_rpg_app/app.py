import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import json
from datetime import datetime
from modules.titles import 称号データ, get_title_info, check_titles
from modules.mission import generate_mission, RECIPE_DB
import time ,os
from datetime import datetime
import random

# ------------------------
# ゾンビ度の理由説明
# ------------------------
def explain_zombie_reason(score):
    if score < 30:
        return "色鮮やかで水分量も十分。腐敗の兆候なし。"
    elif score < 60:
        return "少し色あせてきており、水分が減少傾向。"
    elif score < 80:
        return "明らかな変色と乾燥が見られ、腐敗が進行中。"
    else:
        return "色が黒ずみ、質感も悪化。完全にゾンビ化しています。"

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
                "items_owned": profile.get("items_owned", []),
                "level": profile.get("level", 1),  # ← 追加！
                "exp": profile.get("exp", 0),      # ← 追加！
            })

        else:
            st.error("❌ パスワードが間違っています")
    else:
        st.info("🆕 新規ユーザーとして登録されます")

        # ✅ session_state に初期値を設定
        st.session_state.update({
            "authenticated": True,
            "username": username,
            "password": password,
            "titles": [],
            "missions_completed": [],
            "points": 0,
            "items_owned": [],
            "level": 1,
            "exp": 0
        })

        # ✅ セーブデータ作成と保存
        profile = {
            "username": username,
            "password": password,
            "titles": [],
            "missions_completed": [],
            "points": 0,
            "items_owned": [],
            "level": 1,
            "exp": 0,
            }

        os.makedirs("user_profiles", exist_ok=True)
        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)

        st.success("📝 新規ユーザー登録完了！")

# ------------------------
# 認証後の処理
# ------------------------
if st.session_state.get("authenticated"):
    st.header(f"ようこそ、{st.session_state['username']} さん！")
    st.metric("所持ポイント", f"{st.session_state['points']} pt")

    # レベルと経験値の表示
    level = st.session_state.get("level", 1)
    exp = st.session_state.get("exp", 0)
    next_exp = 100  # レベルアップに必要な経験値

    progress_percent = round((exp / next_exp) * 100, 1)
    st.subheader(f"🧪 今のレベルは Lv.{level} の {progress_percent}% です")
    st.progress(exp / next_exp)
    st.caption(f"経験値：{exp} / {next_exp}")

    # 画像取得方法の選択
    input_method = st.radio("写真の取得方法を選んでください", ["カメラで撮影", "ファイルをアップロード"])

    camera_container = st.container()
    upload_container = st.container()

    image_container = st.empty()

    if input_method == "カメラで撮影":
        image_bytes = image_container.camera_input("野菜の写真を撮ってください", key="main_camera")
    else:
        image_bytes = image_container.file_uploader("野菜の写真をアップロードしてください", type=["png", "jpg", "jpeg"], key="main_uploader")
    # ゾンビ度計算関数
    def calculate_zombie_score(image_bytes):
        img = Image.open(image_bytes)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
        low_saturation = cv2.inRange(hsv, (0, 0, 0), (180, 50, 255))
        zombie_ratio = np.sum(low_saturation > 0) / low_saturation.size
        return round(zombie_ratio * 100, 1)

    if image_bytes:
        # 画像が変わったらリセット
        if st.session_state.get("last_image") != image_bytes:
            st.session_state.pop("fixed_score", None)
            st.session_state.pop("mission_info", None)
            st.session_state["last_image"] = image_bytes
        if "fixed_score" not in st.session_state:
            st.session_state["fixed_score"] = calculate_zombie_score(image_bytes)

        score = st.session_state["fixed_score"]


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
        # ===== 初期化 =====
        for k, v in {
            "points": 0,
            "missions_completed": [],
            "titles": [],
            "items_owned": [],
            "level": 1,
            "exp": 0
        }.items():
            if k not in st.session_state:
                st.session_state[k] = v
        if "mission_info" not in st.session_state:
            st.session_state["mission_info"] = None

        username = st.session_state.get("username", "player")
        password = st.session_state.get("password", "")

        # === 野菜選択肢 =====
        # 通常野菜（レシピDBにあるもの）
        base_veggies = list(RECIPE_DB.keys())

        # ===== 野菜選択UI =====
        available_veggies = base_veggies
        vegetable_name = st.selectbox("撮影した野菜を選んでください", available_veggies)

        # ===== ミッション生成 =====
        def generate_mission(vegetable_name, score):
            bonus = 10 + int(score // 20)
            recipes = RECIPE_DB.get(vegetable_name, [f"{vegetable_name}の定番料理"])
            recipe = random.choice(recipes) if isinstance(recipes, list) else recipes
            return {
                "text": f"{vegetable_name}を使って、『{recipe}』を作れ！",
                "bonus": bonus,
                "recipe": recipe
            }

        # ミッションを一度だけ生成
        # ===== ミッション生成（B仕様：1回の診断中は固定）=====

        # fixed_scoreがなければ作る（＝最初の撮影）
        if "fixed_score" not in st.session_state:
            st.session_state["fixed_score"] = score

        score = st.session_state["fixed_score"]

        # ミッションはまだ無ければ生成
        if st.session_state.get("mission_info") is None:
            st.session_state["mission_info"] = generate_mission(vegetable_name, score)

        # ミッション表示
        if "mission_info" in st.session_state:
            mission_text = st.session_state["mission_info"]["text"]
            base_bonus = st.session_state["mission_info"]["bonus"]

            st.subheader("🎯 今日のミッション")
            st.markdown(mission_text)
        # ===== 証拠画像提出 =====
        proof_container = st.container()
        proof_method = st.radio("証拠画像の取得方法", ["カメラで撮影", "ファイルをアップロード"], key="proof_method")

        if proof_method == "カメラで撮影":
            proof_image = proof_container.camera_input("証拠写真を撮影してください", key="proof_camera")
        else:
            proof_image = proof_container.file_uploader("証拠写真をアップロードしてください", type=["png", "jpg", "jpeg"], key="proof_uploader")

        # ===== ミッション達成処理 =====
        if st.button("✅ ミッション達成！"):
            if vegetable_name and score is not None:

                # ⭐ ここを修正！
                mission_info = st.session_state["mission_info"]
                recipe = mission_info["recipe"]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # ⭐ ポイント加算
                st.session_state["points"] += mission_info["bonus"]
                st.success(f"🎉 {mission_info['bonus']} ポイント獲得！")

                # 証拠画像保存
                proof_path = None
                if proof_image:
                    proof_dir = f"user_profiles/{username}_proofs"
                    os.makedirs(proof_dir, exist_ok=True)
                    proof_path = os.path.join(
                        proof_dir,
                        f"{vegetable_name}_{score}_{timestamp}.jpg"
                    )
                    with open(proof_path, "wb") as f:
                        f.write(proof_image.getbuffer())
                    st.success("📸 証拠画像を保存しました！")

                # ミッション履歴保存
                mission_data = {
                    "vegetable": vegetable_name,
                    "zombie_score": score,
                    "recipe": recipe,
                    "timestamp": timestamp,
                    "proof_path": proof_path
                }
                st.session_state["missions_completed"].append(mission_data)

                # 経験値
                st.session_state["exp"] += 20
                while st.session_state["exp"] >= 100:
                    st.session_state["exp"] -= 100
                    st.session_state["level"] += 1
                    st.success(f"🎉 レベルアップ！Lv.{st.session_state['level']} になりました！")
                    # セーブデータ保存
                    profile_path = f"user_profiles/{username}.json"
                    profile = {
                        "username": username,
                        "password": password,
                        "titles": st.session_state["titles"],
                        "missions_completed": st.session_state["missions_completed"],
                        "points": st.session_state["points"],
                        "items_owned": st.session_state["items_owned"],
                        "level": st.session_state["level"],        
                        "exp": st.session_state["exp"],           
                    }
                    os.makedirs(os.path.dirname(profile_path), exist_ok=True)
                    with open(f"user_profiles/{username}.json", "w", encoding="utf-8") as f:
                        json.dump(profile, f, ensure_ascii=False, indent=2)
                    st.success("💾 セーブデータを保存しました！")
                # ===== 称号獲得チェック =====
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
                        st.markdown(f"""
                        <div style="text-align:center; font-size:28px; color:gold;">
                        🌟 称号進化！<br><br>
                        <span style="font-size:24px;">{進化元} → <strong>{称号}</strong></span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                        old_url = f"https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/{称号データ[進化元]['画像ファイル名']}"
                        new_url = f"https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/{称号データ[称号]['画像ファイル名']}"
                        st.image(old_url, caption=f"旧称号：{進化元}", width=120)
                        st.image(new_url, caption=f"新称号：{称号}", width=150)
                        st.markdown(f"📝 {称号データ[称号]['説明']}")
                    else:
                        st.success(f"🏆 称号獲得：{称号}")
                        st.markdown(称号データ[称号]["説明"])
                        image_url = f"https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/{称号データ[称号]['画像ファイル名']}"
                        st.image(image_url, width=150)
                        st.balloons()

                # 過去のミッション履歴表示
                if st.session_state["missions_completed"]:
                    st.subheader("📜 過去のミッション達成履歴")
                    for m in st.session_state["missions_completed"]:
                        st.markdown(f"{m['vegetable']} → {m['recipe']}（ゾンビ度：{m['zombie_score']}%）")
                        if m.get("proof_path") and os.path.exists(m["proof_path"]):
                            st.image(m["proof_path"], caption="証拠画像", width=200)

                # 次の診断用にリセット
                st.session_state.pop("mission_info", None)
                st.session_state.pop("fixed_score", None)