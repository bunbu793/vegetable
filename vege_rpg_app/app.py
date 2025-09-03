import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import json
from modules.titles import 称号データ, get_title_info
from modules.mission import generate_mission

def explain_zombie_reason(score):
    if score < 30:
        return "画像のほとんどが明るく鮮やかで、腐敗の兆候は見られませんでした。"
    elif score < 60:
        return "一部に暗くくすんだ領域があり、腐敗が始まりつつあると判断されました。"
    elif score < 80:
        return "画像の多くに暗さと低彩度が見られ、腐敗が進行している状態です。"
    else:
        return "画像全体が暗く、色も失われており、完全にゾンビ化していると判定されました。"

st.write("まずはルール説明を読もう！左上にある≫マークをクリックしてメニューを開いてね！そしたら上から3番目の「Rules」を選んでね！")

st.set_page_config(page_title="野菜ゾンビ診断", page_icon="🧟‍♂️")

# セッションステート初期化
st.title("🧟‍♂️ 野菜ゾンビ度診断アプリ")

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
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["titles"] = profile.get("titles", [])
                st.session_state["missions_completed"] = profile.get("missions_completed", [])
            else:
                st.error("❌ パスワードが間違っています")
    else:
        st.info("🆕 新規ユーザーとして登録されます")
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
        st.session_state["titles"] = []
        st.session_state["missions_completed"] = []
if st.session_state.get("authenticated"):
    st.header(f"ようこそ、{st.session_state['username']} さん！")


input_method = st.radio("写真の取得方法を選んでください", ["カメラで撮影", "ファイルをアップロード"])

# 📸 画像取得
image_bytes = None
if input_method == "カメラで撮影":
    image_bytes = st.camera_input("野菜の写真を撮ってください")
else:
    image_bytes = st.file_uploader("野菜の写真をアップロードしてください", type=["png", "jpg", "jpeg"])

# 🧠 ゾンビ度解析関数
def calculate_zombie_score(image_bytes):
    img = Image.open(image_bytes)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)

    # 彩度と明度が低い部分をゾンビ化とみなす
    low_saturation = cv2.inRange(hsv, (0, 0, 0), (180, 50, 255))
    zombie_ratio = np.sum(low_saturation > 0) / low_saturation.size

    return round(zombie_ratio * 100, 1)

# 🧟‍♂️ ゾンビ度診断
if image_bytes:
    st.image(image_bytes, caption="診断対象の野菜", use_container_width=True)
    score = calculate_zombie_score(image_bytes)

    st.progress(score / 100)
    st.metric("ゾンビ度", f"{score}%")

    with st.expander("診断の理由を見る"):
        st.markdown(f"🧠 理由：{explain_zombie_reason(score)}")

    if score < 30:
        st.success("✅ フレッシュ！ゾンビの気配なし。")
    elif score < 60:
        st.warning("⚠️ ややゾンビ化。早めに調理しましょう。")
    elif score < 80:
        st.error("🚨 ゾンビ化進行中！今すぐ炒めて！")
    else:
        st.error("🧟‍♂️ 完全にゾンビ化！冷蔵庫から避難してください！")

    if score < 30:
        st.markdown("🥦「まだ元気だよ！早く食べてね！」")
    elif score < 60:
        st.markdown("🍅「ちょっと疲れてきたかも…」")
    elif score < 80:
        st.markdown("🥕「うぅ…腐りかけてる…」")
    else:
        st.markdown("🧟‍♂️「助けて…もう腐っちゃう…」")


    from modules.mission import generate_mission

if image_bytes:
    vegetable_name = st.selectbox(
    "撮影した野菜を選んでください",
    ["にんじん", "トマト", "キャベツ", "ピーマン", "レタス"]
)
    st.session_state["vegetable_name"] = vegetable_name

    mission = generate_mission(vegetable_name, score)

    mission = generate_mission(vegetable_name, score)

    st.subheader("🎯 今日のミッション")
    st.markdown(mission["mission"])     
    st.session_state["current_mission"] = mission

    # 📸 証拠画像提出UI（ここに入れる！）
    proof_method = st.radio("証拠画像の取得方法", ["カメラで撮影", "ファイルをアップロード"])
    proof_image = None
    if proof_method == "カメラで撮影":
        proof_image = st.camera_input("証拠写真を撮影してください")
    else:
        proof_image = st.file_uploader("証拠写真をアップロードしてください", type=["png", "jpg", "jpeg"])

from modules.titles import check_titles, get_title_info

# 初期化
if "missions_completed" not in st.session_state:
    st.session_state["missions_completed"] = []
if "titles" not in st.session_state:
    st.session_state["titles"] = []

if "missions_completed" not in st.session_state:
    st.session_state["missions_completed"] = []

if st.button("✅ ミッション達成！"):
    st.success("🎉 ミッション完了！ゾンビ野菜を救いました！")
    st.session_state["missions_completed"].append(mission)
    st.balloons()

    # 📸 証拠画像保存処理（ここを追加！）
    if proof_image:
        proof_dir = f"user_profiles/{username}_proofs"
        os.makedirs(proof_dir, exist_ok=True)
        proof_path = os.path.join(proof_dir, f"{vegetable_name}_{score}.jpg")
        with open(proof_path, "wb") as f:
            f.write(proof_image.getbuffer())
        st.success("📸 証拠画像を保存しました！")


    # 🔐 セーブデータ保存処理（ここに書く！）
    import json, os
    profile_path = f"user_profiles/{username}.json"

    profile = {
        "username": username,
        "password": password,
        "titles": st.session_state["titles"],
        "missions_completed": st.session_state["missions_completed"]
    }
    os.makedirs(os.path.dirname(profile_path), exist_ok=True)

    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    st.success("💾 セーブデータを保存しました！")


    # 🏆 称号獲得チェック
    new_titles = check_titles(
        st.session_state["missions_completed"],
        st.session_state["titles"]
    )
    for 称号 in new_titles:
        st.session_state["titles"].append(称号)

        st.markdown("""
        <div style="text-align:center; font-size:24px; color:gold;">
        ✨ 新しい称号を獲得しました ✨
        </div>
        """, unsafe_allow_html=True)

        st.success(f"🏆 称号獲得：{称号}")
        st.markdown(称号データ[称号]["説明"])

        # ✅ 画像表示処理をループの中に入れる！
        # GitHubのraw画像URLを生成
        image_url = f"https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/{称号データ[称号]['画像ファイル名']}"

        # Streamlitで直接表示
        st.image(image_url, width=150)



if st.session_state["missions_completed"]:
    st.subheader("📜 過去のミッション達成履歴")
    for i, m in enumerate(st.session_state["missions_completed"], 1):
        st.markdown(f"{i}. {m['vegetable']} → {m['recipe']}（ゾンビ度：{m['zombie_score']}%）")

        proof_path = f"user_profiles/{username}_proofs/{m['vegetable']}_{m['zombie_score']}.jpg"
        if os.path.exists(proof_path):
            st.image(proof_path, caption="証拠画像", width=200)