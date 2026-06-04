import streamlit as st
from styles import *

import streamlit as st

st.markdown(f"""
    <style>
    .card {{
        {CARD_STYLE}
    }}
    </style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="PAUSE",
    page_icon="assets/logo.png",
    layout="wide"
)

st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 18px;
}

.card{
    background:#0B1220;
    padding:20px;
    border-radius:15px;
    box-shadow:0 2px 8px rgba(0,0,0,0.08);
    height:220px;
}

.stButton button{
    width:100%;
    height:70px;
    font-size:18px;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

st.title("⏸ PAUSE")

st.caption(
    "A collaborative focus platform that helps students "
    "stay productive through structured work sessions."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3>📖 Introduction</h3>
        <p>
        PAUSE is a collaborative productivity platform
        designed to help students manage focus sessions,
        reduce distractions, and build consistent study habits.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>🎯 Objective</h3>
        <p>
        Our goal is to encourage sustainable productivity
        through Pomodoro sessions, analytics, and shared
        focus rooms.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.subheader("⚡ Quick Access")

col1, col2, col3 = st.columns(3, gap="large")

# =========================
# TIMER
# =========================
with col1:
    st.markdown(f"""
    <div class="card">
        <div style="font-size:30px;font-weight:600;color:{TEXT};">
            ⏱ Timer
        </div>
        <div style="font-size:20px;color:{MUTED};margin-top:6px;">
            Pomodoro focus timer with intervals & recovery tracking.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Timer", use_container_width=True):
        st.switch_page("pages/1_Timer.py")

# =========================
# FOCUS ROOM
# =========================
with col2:
    st.markdown(f"""
    <div class="card">
        <div style="font-size:30px;font-weight:600;color:{TEXT};">
            🧘 Focus Room
        </div>
        <div style="font-size:20px;color:{MUTED};margin-top:6px;">
            Minimal distraction workspace for deep focus.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Enter Room", use_container_width=True):
        st.switch_page("pages/2_Focus_room.py")

# =========================
# ANALYTICS
# =========================
with col3:
    st.markdown(f"""
    <div class="card">
        <div style="font-size:30x;font-weight:600;color:{TEXT};">
            📊 Analytics
        </div>
        <div style="font-size:20px;color:{MUTED};margin-top:6px;">
            Track productivity, streaks, burnout & weekly trends.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("View Analytics", use_container_width=True):
        st.switch_page("pages/3_Analytics.py")
