import streamlit as st
import os
import json

# ページ設定
st.set_page_config(page_title="ランキング", page_icon="📊")
st.title("📊 ユーザーランキング")

# ユーザーデータ読み込み関数
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

# ランキング表示
ranking = load_all_profiles()
current_user = st.session_state.get("username", "")

st.markdown("---")
for i, user in enumerate(ranking, 1):
    # 順位ごとのアイコン
    if i == 1:
        icon = "🥇"
    elif i == 2:
        icon = "🥈"
    elif i == 3:
        icon = "🥉"
    else:
        icon = f"{i}位"

    # 自分の順位を強調
    if user["username"] == current_user:
        st.markdown(f"👉 **{icon}：{user['username']}（{user['points']} pt）** ← あなた！")
    else:
        st.markdown(f"{icon}：{user['username']}（{user['points']} pt）")

st.markdown("---")