import streamlit as st
from modules.titles import 称号データ

st.set_page_config(page_title="報酬ショップ", page_icon="🛒")
st.title("🛒 報酬ショップ")

# 所持ポイントの表示
points = st.session_state.get("points", 0)
st.metric("所持ポイント", f"{points} pt")

# 称号ショップのラインナップ（ポイントで購入できる称号）
称号ショップ = {
    "レシピ職人": 30,
    "図鑑研究員": 50,
    "ミッションマニア": 70
}

# 称号購入処理
for title_name, cost in 称号ショップ.items():
    if title_name in st.session_state.get("titles", []):
        st.markdown(f"✅ {title_name}（獲得済み）")
    else:
        st.markdown(f"🛍️ {title_name} — {cost}pt")
        if st.button(f"{title_name} を購入"):
            if points >= cost:
                st.session_state["titles"].append(title_name)
                st.session_state["points"] -= cost
                st.success(f"🏆 {title_name} を獲得しました！")
                image_url = f"https://raw.githubusercontent.com/bunbu793/vegetable/main/vege_rpg_app/assets/images/titles/{称号データ[title_name]['画像ファイル名']}"
                st.image(image_url, width=150)
                st.markdown(f"📝 {称号データ[title_name]['説明']}")
            else:
                st.error("ポイントが足りません")