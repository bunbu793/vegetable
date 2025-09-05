from collections import defaultdict
import streamlit as st
from modules.mission import RECIPE_DB, HIDDEN_VEGETABLES  # ← 必須インポート

st.set_page_config(page_title="野菜図鑑", page_icon="🥬")
st.title("🥬 野菜図鑑")

# --- セッションステートの安全な初期化 ---
if "missions_completed" not in st.session_state:
    st.session_state["missions_completed"] = []
if "items_owned" not in st.session_state:
    st.session_state["items_owned"] = []

# 図鑑表示用の野菜一覧
all_vegetables = list(RECIPE_DB.keys())

# 隠し野菜の解放チェック
for hidden_veg in HIDDEN_VEGETABLES:
    if hidden_veg in st.session_state["items_owned"]:
        all_vegetables.append(hidden_veg)

# --- データがない場合 ---
if not st.session_state["missions_completed"]:
    st.info("まだ野菜を救っていません。診断を行ってミッションを達成しましょう！")

else:
    # ユーザーが救った野菜の種類
    saved_veggies = set(m["vegetable"] for m in st.session_state["missions_completed"])
    # 未救出の野菜
    unsaved_veggies = [v for v in all_vegetables if v not in saved_veggies]
    # コンプリート率
    complete_rate = round(len(saved_veggies) / len(all_vegetables) * 100, 1)

    # --- 表示 ---
    st.subheader("📘 図鑑コンプリート率")
    st.metric("コンプリート率", f"{complete_rate}%")
    st.progress(complete_rate / 100)

    if unsaved_veggies:
        st.subheader("🕵️‍♀️ 未救出の野菜一覧")
        st.markdown("以下の野菜はまだ診断されていません。救出して図鑑を完成させましょう！")
        for veg in unsaved_veggies:
            st.markdown(f"<span style='color:gray;'>🔒 {veg}</span>", unsafe_allow_html=True)
    else:
        st.success("🎉 全ての野菜を救出済みです！図鑑コンプリート！")

    # コメント演出
    if complete_rate == 100:
        st.success("🎉 図鑑コンプリート！全野菜を救いました！")
    elif complete_rate >= 75:
        st.info("あと少しでコンプリート！")
    elif complete_rate >= 50:
        st.warning("半分達成！がんばれ！")
    else:
        st.error("まだまだこれから！野菜を救いに行こう！")

    # 野菜ごとの統計
    veggie_stats = defaultdict(list)
    for m in st.session_state["missions_completed"]:
        veggie_stats[m["vegetable"]].append(m["zombie_score"])

    for veggie, scores in veggie_stats.items():
        avg_score = round(sum(scores) / len(scores), 1)
        count = len(scores)

        # 色分け
        if avg_score < 30:
            color = "green"
        elif avg_score < 60:
            color = "orange"
        elif avg_score < 80:
            color = "red"
        else:
            color = "darkred"

        st.subheader(f"🥕 {veggie}")
        st.markdown(f"<span style='color:{color}; font-size:16px;'>救出回数：{count}回</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:{color}; font-size:16px;'>平均ゾンビ度：{avg_score}%</span>", unsafe_allow_html=True)
        st.progress(avg_score / 100)

    # 救出順に並べた履歴
    st.subheader("📜 救出順に並んだ野菜たち")
    
    sorted_missions = sorted(
        st.session_state["missions_completed"],
        key=lambda m: m.get("timestamp", "")
    )

    for i, m in enumerate(sorted_missions, 1):
        veg = m["vegetable"]
        score = m["zombie_score"]
        timestamp = m.get("timestamp", "日時不明")

        if score < 30:
            color = "green"
        elif score < 60:
            color = "orange"
        elif score < 80:
            color = "red"
        else:
            color = "darkred"

        st.markdown(
            f"<span style='color:{color}; font-size:16px;'>{i}. {veg} → ゾンビ度：{score}%（{timestamp}）</span>",
            unsafe_allow_html=True
        )