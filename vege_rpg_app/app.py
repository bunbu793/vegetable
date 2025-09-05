import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# 1秒ごとにページ再描画
st_autorefresh(interval=1000, key="timer_refresh")

mode = st.radio("モードを選んでね", ["制限時間モード", "ストップウォッチモード"])

# ==============================
# 制限時間モード
# ==============================
if mode == "制限時間モード":
    time_limit_minutes = st.number_input("制限時間（分）", min_value=1, max_value=30, value=5)

    if st.button("🚀 ミッション開始！"):
        st.session_state["mission_start"] = time.time()
        st.session_state["time_limit"] = time_limit_minutes * 60
        st.session_state["mission_active"] = True

    if st.session_state.get("mission_active"):
        elapsed = time.time() - st.session_state["mission_start"]
        remaining = max(st.session_state["time_limit"] - elapsed, 0)
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)

        if remaining <= 60 and remaining > 0:
            st.markdown("<style>.stApp {background-color: #ffcccc;}</style>", unsafe_allow_html=True)

        st.metric("残り時間", f"{minutes}分 {seconds}秒")

        if remaining == 0:
            st.markdown("""
            <style>
            @keyframes blink {0%{opacity:1;}50%{opacity:0;}100%{opacity:1;}}
            .blink {animation: blink 1s infinite; color: red; font-size: 32px; font-weight: bold; text-align: center;}
            </style>
            <div class="blink">💀 GAME OVER 💀</div>
            """, unsafe_allow_html=True)

        if st.button("✅ ミッション達成！"):
            if remaining > 0:
                st.success("⏱ 時間内クリア！+10pt")
                st.session_state["points"] += 10
                st.balloons()
            else:
                st.error("💀 時間切れ！ボーナスなし")
            st.session_state["mission_active"] = False

# ==============================
# ストップウォッチモード
# ==============================
elif mode == "ストップウォッチモード":
    if st.button("🚀 ミッション開始！"):
        st.session_state["mission_start"] = time.time()
        st.session_state["mission_active"] = True

    if st.session_state.get("mission_active"):
        elapsed = time.time() - st.session_state["mission_start"]
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        st.metric("経過時間", f"{minutes}分 {seconds}秒")

        if st.button("✅ ミッション達成！"):
            elapsed = time.time() - st.session_state["mission_start"]

            if elapsed <= 600:
                bonus = 15
                st.success("🥇 超高速クリア！+15pt")
                st.balloons()
            elif elapsed <= 900:
                bonus = 10
                st.success("⏱ 早い！+10pt")
                st.balloons()
            elif elapsed <= 1200:
                bonus = 5
                st.info("👍 ナイス！+5pt")
                st.snow()
            else:
                bonus = 2
                st.warning("お疲れ！+2pt")

            st.session_state["points"] += bonus
            st.session_state["mission_active"] = False