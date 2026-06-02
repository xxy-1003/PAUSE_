import streamlit as st
import time
from datetime import datetime
from storage import init_db, save_session, get_sessions

# ===== SETTINGS =====
with st.sidebar:
    st.header("Settings")

    focus_minutes = st.number_input(
        "Focus Duration (minutes)",
        min_value=1,
        max_value=120,
        value=25
    )

    daily_goal = st.number_input(
        "Daily Goal (sessions)",
        min_value=1,
        max_value=10,
        value=4
    )

FOCUS_DURATION = focus_minutes * 60

# ===== MAIN PAGE =====
st.title("PAUSE Timer MVP")

init_db()

# init state
if "running" not in st.session_state:
    st.session_state.running = False

if "paused" not in st.session_state:
    st.session_state.paused = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0

if "sessions" not in st.session_state:
    st.session_state.sessions = []

if "session_completed" not in st.session_state:
    st.session_state.session_completed = False

if st.session_state.session_completed:
    st.success("Focus Session Complete!")
    st.session_state.session_completed = False

if "history" not in st.session_state:
    st.session_state.history = []

# functions
def start_timer():
    if not st.session_state.running:
        st.session_state.start_time = time.time()
        st.session_state.running = True

def pause_timer():
    if st.session_state.running:
        st.session_state.elapsed += (
            time.time() - st.session_state.start_time
        )

        st.session_state.running = False
        st.session_state.paused = True
        st.session_state.start_time = None

def resume_timer():
    if st.session_state.paused:
        st.session_state.running = True
        st.session_state.paused = False
        st.session_state.start_time = time.time()

def reset_timer():
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.elapsed = 0
    st.session_state.start_time = None

# display placeholder
placeholder = st.empty()

# buttons
col1, col2 = st.columns(2)

with col1:

    if (
        not st.session_state.running
        and not st.session_state.paused
    ):
        if st.button("Start Focus"):
            start_timer()
            st.rerun()

    elif st.session_state.running:
        if st.button("Pause Focus"):
            pause_timer()
            st.rerun()

    elif st.session_state.paused:
        if st.button("Resume Focus"):
            resume_timer()
            st.rerun()

with col2:
    if st.button("Reset"):
        reset_timer()
        st.rerun()

# live timer loop
with placeholder.container():
    if st.session_state.running and st.session_state.start_time is not None:
        current = st.session_state.elapsed + (time.time() - st.session_state.start_time)
    else:
        current = st.session_state.elapsed

    remaining = max(0, FOCUS_DURATION - current)

    if current >= FOCUS_DURATION and st.session_state.running:
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.session_completed = True

        from datetime import datetime

        st.session_state.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration": focus_minutes,
            "status": "COMPLETED"
        })

        save_session(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            focus_minutes,
            "COMPLETED"
        )

        st.rerun()

    mins = int(remaining) // 60
    secs = int(remaining) % 60

    st.metric("Time Left", f"{mins:02d}:{secs:02d}")

if st.session_state.running:
    time.sleep(1)
    st.rerun()

# when paused/stopped
if not st.session_state.running:
    current = st.session_state.elapsed + (
        time.time() - st.session_state.start_time
        if st.session_state.start_time
        else 0
    )

    remaining = FOCUS_DURATION - current

    mins = max(0, int(remaining) // 60)
    secs = max(0, int(remaining) % 60)

    placeholder.metric("Time Left", f"{mins:02d}:{secs:02d}")

completed_sessions = len(st.session_state.history)

# Daily Goal
st.subheader("Daily Goal")
st.write(f"{completed_sessions} / {daily_goal} Sessions")
st.progress(
    min(completed_sessions / daily_goal, 1.0)
)

# Statistics
total_sessions = len(st.session_state.history)
total_focus_time = sum(
    session["duration"]
    for session in st.session_state.history
)

col1, col2 = st.columns(2)
with col1:
    st.metric("Sessions", total_sessions)

with col2:
    st.metric("Focus Time", f"{total_focus_time} min")

# Session History
st.subheader("Session History")
st.write(st.session_state.history)

st.subheader("Database Sessions")
sessions = get_sessions()
st.write(sessions)