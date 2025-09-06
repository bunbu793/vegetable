import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import json
from datetime import datetime
from modules.titles import 称号データ, get_title_info, check_titles
from modules.mission import generate_mission, RECIPE_DB, HIDDEN_VEGETABLES
import time ,os
from datetime import datetime
import random

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

        username = st.session_state.get("username", "player")
        password = st.session_state.get("password", "")

        # ===== アイテムデータ =====
        items_data = {
            "スーパートマトジュース": {"説明": "ポイント+5", "必要レベル": 1, "効果": {"points": 5}},
            "黄金のニンジン": {"説明": "称号獲得率UP", "必要レベル": 3, "効果": {"title_boost": True}},
            "伝説のカボチャ": {"説明": "ポイント+20", "必要レベル": 5, "効果": {"points": 20}}
        }

        # ===== レア野菜データ =====
        if "rare_veggies_data" not in st.session_state:
            st.session_state["rare_veggies_data"] = {
                "白いナス": {"説明": "希少なナス。特別ミッションで使用可能", "解放済み": False},
                "紫色のカリフラワー": {"説明": "ポイントボーナス付き", "解放済み": False},
                "黄金のトマト": {"説明": "称号獲得率UP", "解放済み": False}
            }

        # === 野菜選択肢 =====
        base_veggies = list(RECIPE_DB.keys())
        rare_veggies_unlocked = [
            name for name, data in st.session_state["rare_veggies_data"].items()
            if data["解放済み"]
        ]
        available_veggies = base_veggies + rare_veggies_unlocked

        # ===== 野菜選択UI =====
        vegetable_name = st.selectbox("撮影した野菜を選んでください", available_veggies)

        # ===== ミッション生成 =====
        def generate_mission(vegetable_name):
            if vegetable_name in st.session_state["rare_veggies_data"]:
                return f"🌟 特別ミッション！{vegetable_name}を使って料理を作れ！", 20
            else:
                return f"{vegetable_name}を使った料理を作れ！", 10

        mission_text, base_bonus = generate_mission(vegetable_name)
        st.subheader("🎯 今日のミッション")
        st.markdown(mission_text)

        # ===== レア野菜ミニゲーム =====
        def rare_veggie_minigame(vegetable_name, base_bonus):
            st.info(f"🎮 {vegetable_name} 料理シミュレーション開始！")

            method = st.radio("調理法を選ぼう", ["焼く", "煮る", "生で食べる"], key="method")
            ingredient = st.selectbox("追加食材を選ぼう", ["チーズ", "ベーコン", "はちみつ"], key="ingredient")
            seasoning = st.radio("味付けを選ぼう", ["塩コショウ", "カレー風味", "甘辛ソース"], key="seasoning")

            if st.button("料理完成！", key="cook_btn"):
                outcome = random.choice(["大成功！", "まあまあ", "失敗…"])
                st.success(f"{outcome} {method} {ingredient} {seasoning} の {vegetable_name}料理が完成！")

                bonus = base_bonus
                if outcome == "大成功！":
                    bonus += 10
                    st.balloons()

                st.session_state["points"] += bonus
                st.success(f"🎁 ボーナス {bonus}pt（合計：{st.session_state['points']}pt）")
                return bonus
            return None

        # ===== 証拠画像提出 =====
        proof_method = st.radio("証拠画像の取得方法", ["カメラで撮影", "ファイルをアップロード"])
        proof_image = (
            st.camera_input("証拠写真を撮影してください") if proof_method == "カメラで撮影"
            else st.file_uploader("証拠写真をアップロードしてください", type=["png", "jpg", "jpeg"])
        )

        # ===== ミッション達成処理 =====
        if st.button("✅ ミッション達成！"):
            bonus = base_bonus
            mission_data = {
                "vegetable": vegetable_name,
                "zombie_score": score,
                "recipe": recipe,
                "timestamp": datetime.now().strftime("%Y%m%d%H%M%S")
            }

            if vegetable_name in st.session_state["rare_veggies_data"]:
                result = rare_veggie_minigame(vegetable_name, base_bonus)
                if result is not None:
                    bonus = result
            else:
                st.session_state["points"] += base_bonus
                st.success(f"🎁 報酬ポイント +{base_bonus}pt（合計：{st.session_state['points']}pt）")
                st.balloons()

            # 証拠画像保存
            if proof_image:
                proof_dir = f"user_profiles/{username}_proofs"
                os.makedirs(proof_dir, exist_ok=True)
                proof_path = os.path.join(
                    proof_dir,
                    f"{vegetable_name}_{bonus}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                )
                with open(proof_path, "wb") as f:
                    f.write(proof_image.getbuffer())
                st.success("📸 証拠画像を保存しました！")

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
                "rare_veggies_data": st.session_state["rare_veggies_data"]
            }
            os.makedirs(os.path.dirname(profile_path), exist_ok=True)
            with open(profile_path, "w", encoding="utf-8") as f:
                json.dump(profile, f, ensure_ascii=False, indent=2)
            st.success("💾 セーブデータを保存しました！")

        # ===== アイテム一覧表示 =====
        st.subheader("🎁 アイテム一覧")
        for name, data in items_data.items():
            if st.session_state["level"] >= data["必要レベル"]:
                st.write(f"🛒 {name} - {data['説明']}")
            else:
                st.write(f"🔒 {name} - {data['必要レベル']}レベルで解放")
                st.markdown("アイテムは「アイテムショップ」ページで購入できます。")

        # ===== 称号獲得チェック =====
        if "check_titles" in globals():
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
                for i, m in enumerate(st.session_state["missions_completed"], 1):
                    st.markdown(f"{i}. {m['vegetable']} → {m['recipe']}（ゾンビ度：{m['zombie_score']}%）")
                    "user_profiles/{username}_proofs/{m['vegetable']}_{m['zombie_score']}_{m['timestamp']}.jpg"
                    if os.path.exists(proof_path):
                        st.image(proof_path, caption="証拠画像", width=200)