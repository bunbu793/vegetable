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

# 期間別ランキング抽出
def get_period_ranking(period="week"):
    history = load_ranking_history()
    now = datetime.now()
    filtered = []

    for entry in history:
        ts = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        if period == "week" and ts.isocalendar()[1] == now.isocalendar()[1] and ts.year == now.year:
            filtered.append(entry)
        elif period == "month" and ts.month == now.month and ts.year == now.year:
            filtered.append(entry)

    ranking = {}
    for entry in filtered:
        ranking[entry["username"]] = entry["points"]
    return sorted(ranking.items(), key=lambda x: x[1], reverse=True)

# 通常ランキング（最新ポイント）
def load_all_profiles():
    profiles = []
    for filename in os.listdir("user_profiles"):
        if filename.endswith(".json"):
            with open(os.path.join("user_profiles", filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                profiles.append({
                    "username": data.get("username", "unknown"),
                    "points": data.get("points", 0)
                })
    return sorted(profiles, key=lambda x: x["points"], reverse=True)

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

show_ranking("📅 今週のランキング", get_period_ranking("week"), current_user)
show_ranking("🗓️ 今月のランキング", get_period_ranking("month"), current_user)