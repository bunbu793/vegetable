import pandas as pd
import altair as alt  # グラフを色付きで表示するなら
import streamlit as st

st.set_page_config(page_title="診断履歴グラフ", page_icon="📊")
st.title("📊 ゾンビ度の診断履歴")

# セッションステート確認
if "missions_completed" not in st.session_state or not st.session_state["missions_completed"]:
    st.info("まだミッション履歴がありません。診断を行ってミッションを達成しましょう！")
else:
    # ゾンビ度履歴を抽出
    scores = [m["zombie_score"] for m in st.session_state["missions_completed"]]
    veggies = [m["vegetable"] for m in st.session_state["missions_completed"]]

    avg_score = round(sum(scores) / len(scores), 1)
    max_score = max(scores)

    st.metric("平均ゾンビ度", f"{avg_score}%")
    st.metric("最高ゾンビ度", f"{max_score}%")

    def score_comment(score):
        if score < 30:
            return "<span style='color:green;'>フレッシュな診断が多いです！</span>"
        elif score < 60:
            return "<span style='color:orange;'>ややゾンビ化傾向があります。</span>"
        elif score < 80:
            return "<span style='color:red;'>ゾンビ化が進行しています。</span>"
        else:
            return "<span style='color:darkred;'>危険！ゾンビ野菜が大量発生中！</span>"

    st.markdown(score_comment(avg_score), unsafe_allow_html=True)
    df = pd.DataFrame({
        "回数": list(range(1, len(scores)+1)),
        "ゾンビ度": scores,
        "野菜": veggies
    })

    chart = alt.Chart(df).mark_line(point=True).encode(
        x="回数",
        y="ゾンビ度",
        color="野菜"
    ).properties(width=700)

    # グラフ表示
    st.subheader("ゾンビ度の推移")
    st.altair_chart(chart)

    # 詳細表示
    st.subheader("履歴一覧")
    for i, (veg, score) in enumerate(zip(veggies, scores), 1):
        st.markdown(f"{i}. {veg} → ゾンビ度：{score}%")

        st.subheader("📜 詳細な履歴")
        with st.expander("履歴を見る"):
            for i, m in enumerate(st.session_state["missions_completed"], 1):
                score = m["zombie_score"]
                if score < 30:
                    color = "green"
                elif score < 60:
                    color = "orange"
                elif score < 80:
                    color = "red"
                else:
                    color = "darkred"

                st.markdown(
                    f"<span style='color:{color}; font-size:16px;'>{i}. {m['vegetable']} → ゾンビ度：{score}%（{m['timestamp']}）</span>",
                    unsafe_allow_html=True
                )