import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="ランキング", page_icon="📊")
st.title("📊 ユーザーランキング")

# 履歴読み込み関数
def load_ranking_history():
    history_path = "data/ranking_history.json"
    if not os.path.exists(history_path):
        return []
    with open(history_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ranking_entry(username, points):
    history_path = "data/ranking_history.json"
    os.makedirs("data", exist_ok=True)
    history = load_ranking_history()
    history.append({
        "username": username,
        "points": points,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# 期間別ランキング抽出
def get_period_ranking(period="week"):
    history = load_ranking_history()
    now = datetime.now()
    filtered = []

    for entry in history:
        ts = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        if period == "day" and ts.date() == now.date():
            filtered.append(entry)
        elif period == "week" and ts.isocalendar()[1] == now.isocalendar()[1] and ts.year == now.year:
            filtered.append(entry)
        elif period == "month" and ts.month == now.month and ts.year == now.year:
            filtered.append(entry)
        elif period == "year" and ts.year == now.year:
            filtered.append(entry)
    
    # ユーザーごとの最新ポイントを集計
    ranking = {}
    for entry in filtered:
        ranking[entry["username"]] = ranking.get(entry["username"], 0) + entry["points"]

    return sorted(ranking.items(), key=lambda x: x[1], reverse=True)


# 表示関数
def show_ranking(title, ranking, current_user):
    st.subheader(title)
    if not ranking:
        st.info("まだランキングデータがありません")
        return
    for i, (user, pts) in enumerate(ranking, 1):
        icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}位"
        if user == current_user:
            st.markdown(f"👉 **{icon}：{user}（{pts} pt）** ← あなた！")
        else:
            st.markdown(f"{icon}：{user}（{pts} pt）")

# 実行
current_user = st.session_state.get("username", "")

show_ranking("📅 今日のランキング", get_period_ranking("day"), current_user )
show_ranking("📅 今週のランキング", get_period_ranking("week"), current_user)
show_ranking("🗓️ 今月のランキング", get_period_ranking("month"), current_user)
show_ranking("📆 今年のランキング", get_period_ranking("year"), current_user)

# ランキング履歴追加フォーム
with st.form("add_entry"):
    st.subheader("📝 ランキング履歴に追加")
    name = st.text_input("ユーザー名")
    pts = st.number_input("ポイント", min_value=0)
    submitted = st.form_submit_button("ランキングに追加")
    if submitted:
        save_ranking_entry(name, pts)
        st.success("ランキング履歴に追加しました！")

st.write("📜 履歴データ:", load_ranking_history())
st.write("ℹ️ 注意：ランキングは手動で追加する形式です。実際のゲームプレイに連動していません。")