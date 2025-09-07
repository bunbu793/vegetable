import streamlit as st

st.set_page_config(page_title="素材売却所", page_icon="💸")
st.title("💸 素材売却所")

# 初期化（念のため）
if "owned_veggies" not in st.session_state:
    st.session_state["owned_veggies"] = {}
if "owned_seasonings" not in st.session_state:
    st.session_state["owned_seasonings"] = {}
if "money" not in st.session_state:
    st.session_state["money"] = 0

# 売却価格設定
veggie_sell_prices = {
    "トマト": 10, "ナス": 8, "チーズ": 20, "キャベツ": 6, "ニンジン": 5,
    "ジャガイモ": 7, "ピーマン": 6, "カボチャ": 12
}
seasoning_sell_prices = {
    "塩": 3, "砂糖": 3, "醤油": 5, "スパイス": 8, "オリーブオイル": 10
}

# 合計売却金額の計算
total_sell = 0
sell_summary = []

# 野菜売却処理
for veggie, count in st.session_state["owned_veggies"].items():
    if count > 0 and veggie in veggie_sell_prices:
        price = veggie_sell_prices[veggie]
        total_sell += price * count
        sell_summary.append(f"{veggie}（x{count}）→ ¥{price * count}")

# 調味料売却処理
for seasoning, count in st.session_state["owned_seasonings"].items():
    if count > 0 and seasoning in seasoning_sell_prices:
        price = seasoning_sell_prices[seasoning]
        total_sell += price * count
        sell_summary.append(f"{seasoning}（x{count}）→ ¥{price * count}")

# 売却ボタン
if total_sell > 0:
    if st.button(f"🧺 まとめて売却（合計 ¥{total_sell}）"):
        for veggie in list(st.session_state["owned_veggies"].keys()):
            st.session_state["owned_veggies"][veggie] = 0
        for seasoning in list(st.session_state["owned_seasonings"].keys()):
            st.session_state["owned_seasonings"][seasoning] = 0
        st.session_state["money"] += total_sell
        st.success("✅ すべての素材を売却しました！")
        st.markdown("🧾 売却内容：\n" + "\n".join(sell_summary))
        st.experimental_rerun()
else:
    st.info("🧺 売却できる素材がありません。")

st.markdown("---")
st.metric("現在の所持金", f"🪙{st.session_state['money']}マネー")