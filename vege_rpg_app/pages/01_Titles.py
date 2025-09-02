import streamlit as st
from modules.titles import 称号データ, get_title_info

st.set_page_config(page_title="称号一覧", page_icon="🏆")
st.title("🏆 あなたの称号コレクション")

if "titles" not in st.session_state:
    st.session_state["titles"] = []

# 称号一覧表示（全称号をループ）
for title_name in 称号データ.keys():
    if title_name in st.session_state["titles"]:
        # 獲得済みの称号
        st.subheader(f"🏅 {title_name}")
        st.markdown(get_title_info(title_name))
        image_url = f"https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/{称号データ[title_name]['画像ファイル名']}"
        st.image(image_url, width=150)


    else:
        # 未獲得の称号（グレー表示）
        st.subheader("🔒 ???")
        st.markdown("条件未達成の称号です")
        
        import os
        image_path = f"assets/images/titles/{称号データ[title_name]['画像ファイル名']}" 

        st.image("https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/locked.png", width=150)
        if os.path.exists(image_path):
            st.image(image_path, width=150)
