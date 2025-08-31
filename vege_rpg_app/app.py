import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import json
from modules.titles import 称号データ, get_title_info



st.set_page_config(page_title="野菜ゾンビ診断", page_icon="🧟‍♂️")

theme = st.selectbox("テーマを選択", ["ホラー", "ファンタジー", "和風"])

if theme == "ホラー":
    st.markdown("<style>body { background-color: #1a1a1a; color: red; }</style>", unsafe_allow_html=True)
elif theme == "ファンタジー":
    st.markdown("<style>body { background-color: #f0f8ff; color: purple; }</style>", unsafe_allow_html=True)
elif theme == "和風":
    st.markdown("<style>body { background-color: #fffaf0; color: darkgreen; }</style>", unsafe_allow_html=True)

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

    if score < 30:
        st.success("✅ フレッシュ！ゾンビの気配なし。")
    elif score < 60:
        st.warning("⚠️ ややゾンビ化。早めに調理しましょう。")
    elif score < 80:
        st.error("🚨 ゾンビ化進行中！今すぐ炒めて！")
    else:
        st.error("🧟‍♂️ 完全にゾンビ化！冷蔵庫から避難してください！" )

    if score < 30:
        st.markdown("🥦「まだ元気だよ！早く食べてね！」")
    elif score < 60:
        st.markdown("🍅「ちょっと疲れてきたかも…」")
    elif score < 80:
        st.markdown("🥕「うぅ…腐りかけてる…」")
    else:
        st.markdown("🧟‍♂️「助けて…もう腐っちゃう…」")


    from modules.mission import generate_mission
    vegetable_name = st.selectbox(
    "撮影した野菜を選んでください",
    ["にんじん", "トマト", "キャベツ", "ピーマン", "レタス"]
)

    mission = generate_mission(vegetable_name, score)

    st.subheader("🎯 今日のミッション")
    st.markdown(mission["mission"])     
    st.session_state["current_mission"] = mission

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

    # 🔐 セーブデータ保存処理（ここに書く！）
    import json, os
    profile_path = f"user_profiles/{username}.json"

    profile = {
        "username": username,
        "password": password,
        "titles": st.session_state["titles"],
        "missions_completed": st.session_state["missions_completed"]
    }

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
        image_path = f"assets/images/titles/{称号データ[称号]['画像ファイル名']}"
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                st.image(img, width=150)
            except Exception as e:
                st.warning(f"画像の読み込みに失敗しました：{e}")
        else:
            st.warning(f"画像ファイルが見つかりません：{image_path}")


if st.session_state["missions_completed"]:
    st.subheader("📜 過去のミッション達成履歴")
    for i, m in enumerate(st.session_state["missions_completed"], 1):
        st.markdown(f"{i}. {m['vegetable']} → {m['recipe']}（ゾンビ度：{m['zombie_score']}%）")