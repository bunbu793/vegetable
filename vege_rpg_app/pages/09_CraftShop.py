import streamlit as st

st.set_page_config(page_title="ショップ", page_icon="🛍️")
st.title("🛍️ 野菜＆調味料ショップ")

# 初期化
if "money" not in st.session_state:
    st.session_state["money"] = 100
if "available_veggies" not in st.session_state:
    st.session_state["available_veggies"] = []
if "seasonings" not in st.session_state:
    st.session_state["seasonings"] = []

# 商品リスト（価格付き）
veggie_store = {
    "トマト": 20, "ナス": 15, "キャベツ": 10, "ニンジン": 10, "ジャガイモ": 12,
    "チーズ": 30, "カボチャ": 18
}
seasoning_store = {
    "塩": 5, "砂糖": 5, "醤油": 8, "スパイス": 12, "オリーブオイル": 15
}

def add_veggie(veggie_name, quantity=1):
    if "owned_veggies" not in st.session_state:
        st.session_state["owned_veggies"] = {}
    st.session_state["owned_veggies"][veggie_name] = st.session_state["owned_veggies"].get(veggie_name, 0) + quantity

def add_seasoning(seasoning_name, quantity=1):
    if "owned_seasonings" not in st.session_state:
        st.session_state["owned_seasonings"] = {}
    st.session_state["owned_seasonings"][seasoning_name] = st.session_state["owned_seasonings"].get(seasoning_name, 0) + quantity

st.subheader("🥦 野菜を購入")
for veggie, price in veggie_store.items():
    if st.button(f"{veggie} を購入（🪙{price}）マネー"):
        if st.session_state["money"] >= price:
            st.session_state["money"] -= price
            add_veggie(veggie)
            st.success(f"{veggie} を購入しました！")
        else:
            st.error("💸 マネーが足りません！")

st.subheader("🧂 調味料を購入")
for seasoning, price in seasoning_store.items():
    if st.button(f"{seasoning} を購入（🪙{price}）マネー"):
        if st.session_state["money"] >= price:
            st.session_state["money"] -= price
            add_seasoning(seasoning)
            st.success(f"{seasoning} を購入しました！")
        else:
            st.error("💸 マネーが足りません！")


st.markdown("---")
st.metric("現在の所持金", f"🪙{st.session_state['money']}マネー")