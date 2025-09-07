import streamlit as st
from modules.items import ITEMS_DB

st.set_page_config(page_title="アイテムショップ", page_icon="🧪")
st.title("🧪 アイテムショップ")

points = st.session_state.get("points", 0)
st.metric("所持ポイント", f"{points} pt")

if "items_owned" not in st.session_state:
    st.session_state["items_owned"] = []

# ===== アイテム購入処理 =====
for item_name, data in ITEMS_DB.items():
    st.subheader(f"{item_name} — {data['価格']}pt")
    st.markdown(data["説明"])
    if item_name in st.session_state["items_owned"]:
        st.markdown("✅ 所持済み")
    elif st.button(f"{item_name} を購入", key=f"buy_{item_name}"):
        if points >= data["価格"]:
            st.session_state["points"] -= data["価格"]