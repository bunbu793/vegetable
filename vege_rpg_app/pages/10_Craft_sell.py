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

if "sold" not in st.session_state:
    st.session_state["sold"] = False
if "sell_summary" not in st.session_state:
    st.session_state["sell_summary"] = []

# 売却ボタン
if total_sell > 0:
    if st.button(f"🧺 まとめて売却（合計 ¥{total_sell}）"):
        for veggie in st.session_state["owned_veggies"]:
            st.session_state["owned_veggies"][veggie] = 0
        for seasoning in st.session_state["owned_seasonings"]:
            st.session_state["owned_seasonings"][seasoning] = 0
        st.session_state["money"] += total_sell
        st.session_state["sold"] = True
        st.session_state["sell_summary"] = sell_summary

# 売却結果の表示
if st.session_state["sold"]:
    st.success("✅ すべての素材を売却しました！")
    st.markdown("🧾 売却内容：\n" + "\n".join(st.session_state["sell_summary"]))
    st.session_state["sold"] = False  # リセット
elif not st.session_state["sold"]:
    st.info("🧺 売却できる素材がありません。")
st.subheader("🥦 野菜の個別売却")

for veggie, count in st.session_state["owned_veggies"].items():
    if count > 0 and veggie in veggie_sell_prices:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.write(f"{veggie}（x{count}）")
        with col2:
            qty = st.number_input(f"{veggie} 売却数", min_value=0, max_value=count, key=f"{veggie}_qty")
        with col3:
            if st.button(f"{veggie}を売却", key=f"{veggie}_sell"):
                if qty > 0:
                    price = veggie_sell_prices[veggie]
                    st.session_state["owned_veggies"][veggie] -= qty
                    st.session_state["money"] += price * qty
                    st.success(f"{veggie}を {qty}個 売却しました！（+¥{price * qty}）")
                else:
                    st.warning("⚠️ 売却数は1以上にしてください")

st.subheader("🧂 調味料の個別売却")

for seasoning, count in st.session_state["owned_seasonings"].items():
    if count > 0 and seasoning in seasoning_sell_prices:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.write(f"{seasoning}（x{count}）")
        with col2:
            qty = st.number_input(f"{seasoning} 売却数", min_value=0, max_value=count, key=f"{seasoning}_qty")
        with col3:
            if st.button(f"{seasoning}を売却", key=f"{seasoning}_sell"):
                if qty > 0:
                    price = seasoning_sell_prices[seasoning]
                    st.session_state["owned_seasonings"][seasoning] -= qty
                    st.session_state["money"] += price * qty
                    st.success(f"{seasoning}を {qty}個 売却しました！（+¥{price * qty}）")
                else:
                    st.warning("⚠️ 売却数は1以上にしてください")

st.markdown("---")
st.metric("現在の所持金", f"🪙{st.session_state['money']}マネー")