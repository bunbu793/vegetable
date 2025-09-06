import streamlit as st
from modules.items import ITEMS_DB

# ===== レア野菜データ =====
rare_veggies_data = {
    "① 白いナス": {"説明": "希少なナス。特別ミッションで使用可能", "解放済み": False},
    "② 紫色のカリフラワー": {"説明": "ポイントボーナス付き", "解放済み": False},
    "③ 黄金のトマト": {"説明": "称号獲得率UP", "解放済み": False}
}

st.set_page_config(page_title="アイテムショップ", page_icon="🧪")
st.title("🧪 アイテムショップ")

points = st.session_state.get("points", 0)
st.metric("所持ポイント", f"{points} pt")

if "items_owned" not in st.session_state:
    st.session_state["items_owned"] = []

if "rare_unlock_ticket" not in st.session_state:
    st.session_state["rare_unlock_ticket"] = 0

# ===== アイテム購入処理 =====
for item_name, data in ITEMS_DB.items():
    st.subheader(f"{item_name} — {data['価格']}pt")
    st.markdown(data["説明"])
    if item_name in st.session_state["items_owned"]:
        st.markdown("✅ 所持済み")
    elif st.button(f"{item_name} を購入", key=f"buy_{item_name}"):
        if points >= data["価格"]:
            st.session_state["points"] -= data["価格"]

            # 特殊処理：レア野菜解放券
            if item_name == "レア野菜解放券":
                st.session_state["rare_unlock_ticket"] += 1
                st.success(f"{item_name} を購入しました！ 🎫 現在 {st.session_state['rare_unlock_ticket']} 枚")
            else:
                st.session_state["items_owned"].append(item_name)
                st.success(f"{item_name} を購入しました！")
        else:
            st.error("ポイントが足りません")

# ===== レア野菜解放UI =====
if st.session_state["rare_unlock_ticket"] > 0:
    st.subheader("🎫 レア野菜解放")
    locked_veggies = [name for name, data in rare_veggies_data.items() if not data["解放済み"]]
    if locked_veggies:
        choice = st.radio("解放するレア野菜を選んでください", locked_veggies, key="unlock_choice")
        if st.button("このレア野菜を解放する", key="unlock_btn"):
            rare_veggies_data[choice]["解放済み"] = True
            st.session_state["rare_unlock_ticket"] -= 1
            st.success(f"🥦 {choice} を解放しました！")
    else:
        st.info("すべてのレア野菜が解放済みです")