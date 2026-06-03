import streamlit as st
import time
from datetime import datetime, timedelta
from storage import init_db, save_session, get_sessions

# =========================
# STATE INIT
# =========================
if "mode" not in st.session_state:
    st.session_state.mode = "focus"

if "running" not in st.session_state:
    st.session_state.running = False

if "paused" not in st.session_state:
    st.session_state.paused = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "cycle_count" not in st.session_state:
    st.session_state.cycle_count = 0

if "focus_elapsed_before_break" not in st.session_state:
    st.session_state.focus_elapsed_before_break = 0

if "interval_taken" not in st.session_state:
    st.session_state.interval_taken = False

if "break_type" not in st.session_state:
    st.session_state.break_type = "normal"

if "break_duration" not in st.session_state:
    st.session_state.break_duration = 5 * 60

def get_current_time():
    if st.session_state.start_time:
        return st.session_state.elapsed + (time.time() - st.session_state.start_time)
    return st.session_state.elapsed

# =========================
# SETTINGS INPUT
# =========================
with st.sidebar:

    if "daily_goal" not in st.session_state:
        st.session_state.daily_goal = 4

    focus_minutes = st.number_input(
        "Focus Duration (minutes)",
        min_value=1,
        max_value=120,
        value=25
    )

    break_minutes = st.number_input(
        "Recovery Duration (minutes)",
        min_value=1,
        max_value=30,
        value=5
    )

    interval_break_minutes = st.number_input(
        "Interval Break Duration (minutes)",
        min_value=1,
        max_value=15,
        value=3
    )

    interval_minutes = st.number_input(
        "Interval Break Frequency (minutes)",
        min_value=1,
        max_value=60,
        value=30
    )

    st.session_state.daily_goal = st.number_input(
        "Daily Goal (sessions)",
        min_value=1,
        max_value=10,
        value=st.session_state.daily_goal
    )


# =========================
# DURATIONS
# =========================
FOCUS_DURATION = focus_minutes * 60
BREAK_DURATION = break_minutes * 60
INTERVAL_BREAK_DURATION = interval_break_minutes * 60
INTERVAL = interval_minutes * 60

# =========================
# MODE
# =========================
if st.session_state.mode == "focus":
    ACTIVE_DURATION = FOCUS_DURATION
    label = "Focus Time"

elif st.session_state.break_type == "interval":
    ACTIVE_DURATION = INTERVAL_BREAK_DURATION
    label = "Interval Break"

else:
    ACTIVE_DURATION = BREAK_DURATION
    label = "Recovery Time"

# # =========================
# # OVERLAY STATE SYNC
# # =========================
# def is_focus_active():
#     return st.session_state.mode == "focus"

# def is_running():
#     return st.session_state.running

# def is_locked():
#     return is_focus_active() and is_running()

# # =========================
# # OVERLAY UI (IMPORTANT: MUST BE ABOVE USAGE)
# # =========================
# def render_overlay(remaining, label):

#     mins = int(remaining) // 60
#     secs = int(remaining) % 60

#     st.markdown(f"""
#     <style>
#     .focus-overlay {{
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         background: rgba(0,0,0,0.35);
#         backdrop-filter: blur(6px);
#         z-index: 9999;
#         display: flex;
#         justify-content: center;
#         align-items: center;
#     }}

#     .focus-box {{
#         background: rgba(20,20,20,0.95);
#         padding: 40px 60px;
#         border-radius: 20px;
#         text-align: center;
#         color: white;
#         min-width: 320px;
#         box-shadow: 0 10px 40px rgba(0,0,0,0.4);
#     }}

#     .time {{
#         font-size: 64px;
#         font-weight: bold;
#         margin-top: 10px;
#     }}
#     </style>

#     <div class="focus-overlay">
#         <div class="focus-box">
#             <h2>{label}</h2>
#             <div class="time">{mins:02d}:{secs:02d}</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# # =========================
# # OVERLAY CONTROLLER (FIXED ORDER)
# # =========================
# locked = is_locked()

# if locked:
#     current = get_current_time()
#     remaining = max(0, FOCUS_DURATION - current)
#     render_overlay(remaining, "Focus Mode")

# # =========================
# # OVERLAY BUTTON
# # =========================
# if locked:
#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("Pause"):
#             pause_timer()
#             st.rerun()

#     with col2:
#         if st.button("Exit"):
#             ...
#             st.rerun()

# =========================
# MAIN
# =========================
st.title("PAUSE Timer MVP")
init_db()

# =========================
# FUNCTIONS
# =========================
def start_timer():
    if not st.session_state.running:
        st.session_state.start_time = time.time()
        st.session_state.running = True
        st.session_state.paused = False
        st.rerun()

def pause_timer():
    if st.session_state.running and st.session_state.start_time:
        st.session_state.elapsed += time.time() - st.session_state.start_time
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

st.subheader(f"🧠 {label}")
placeholder = st.empty()

# =========================
# BUTTONS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    if not st.session_state.running and not st.session_state.paused:
        if st.button("Start"):
            start_timer()
            st.rerun()

    elif st.session_state.running:
        if st.button("Pause"):
            pause_timer()
            st.rerun()

    elif st.session_state.paused:
        if st.button("Resume"):
            resume_timer()
            st.rerun()

with col2:
    if st.button("Reset"):
        reset_timer()
        st.rerun()

with col3:
    if st.button("Switch Mode"):
        st.session_state.mode = "break" if st.session_state.mode == "focus" else "focus"
        st.session_state.elapsed = 0
        st.session_state.start_time = None
        st.rerun()

# =========================
# TIMER LOOP
# =========================
with placeholder.container():

    if st.session_state.running and st.session_state.start_time:
        current = get_current_time()
    else:
        current = st.session_state.elapsed

    remaining = max(0, ACTIVE_DURATION - current)

    # =========================
    # INTERVAL BREAK DONE
    # =========================
    if (
        st.session_state.mode == "break"
        and st.session_state.break_type == "interval"
        and current >= INTERVAL_BREAK_DURATION
    ):
        st.session_state.mode = "focus"
        st.session_state.elapsed = st.session_state.focus_elapsed_before_break
        st.session_state.start_time = time.time()
        st.session_state.running = True
        st.session_state.paused = False
        st.rerun()

    # =========================
    # NORMAL BREAK DONE 
    # =========================
    elif (
        st.session_state.mode == "break"
        and st.session_state.break_type == "normal"
        and current >= BREAK_DURATION
    ):
        save_session(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            break_minutes,   # ✅ FIX: real duration
            "BREAK_COMPLETED"
        )

        st.session_state.mode = "focus"
        st.session_state.elapsed = 0
        st.session_state.start_time = time.time()
        st.session_state.running = True
        st.session_state.paused = False
        st.rerun()

    # =========================
    # FOCUS DONE 
    # =========================
    elif current >= FOCUS_DURATION and st.session_state.running:

        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.interval_taken = False

        st.session_state.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration": focus_minutes,
            "status": "FOCUS_COMPLETED"
        })

        save_session(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            focus_minutes,
            "FOCUS_COMPLETED"   
        )

        st.session_state.cycle_count += 1
        break_time = 15 if st.session_state.cycle_count % 4 == 0 else 5

        st.session_state.break_duration = break_time * 60
        st.session_state.mode = "break"
        st.session_state.break_type = "normal"

        st.session_state.elapsed = 0
        st.session_state.start_time = time.time()
        st.session_state.running = True
        st.session_state.paused = False

        st.rerun()

    mins = int(remaining) // 60
    secs = int(remaining) % 60
    timer_placeholder = st.empty()

    with timer_placeholder:
        st.metric("Time Left", f"{mins:02d}:{secs:02d}")

# =========================
# AUTO TIMER REFRESH 
# =========================
if st.session_state.running:
    time.sleep(0.2)
    st.rerun()

# =========================
# DATABASE STATS
# =========================
today = datetime.now().date() 

sessions = get_sessions()

completed_sessions = len([
    s for s in sessions
    if (
        s[2] in ["COMPLETED", "FOCUS_COMPLETED"]
        and datetime.strptime(
            s[0],
            "%Y-%m-%d %H:%M:%S"
        ).date() == today
    )
])

progress = (
    completed_sessions / st.session_state.daily_goal
    if st.session_state.daily_goal else 0
)

total_focus_time = sum(
    int(s[1])
    for s in sessions
    if (
        s[2] in ["COMPLETED", "FOCUS_COMPLETED"]
        and datetime.strptime(
            s[0],
            "%Y-%m-%d %H:%M:%S"
        ).date() == today
    )
)

# =========================
# STREAK FIXED
# =========================
daily_count = {}

for s in sessions:
    if s[2] not in ["COMPLETED", "FOCUS_COMPLETED"]:
        continue

    try:
        d = datetime.strptime(
            s[0],
            "%Y-%m-%d %H:%M:%S"
        ).date()
        daily_count[d] = daily_count.get(d, 0) + 1

    except:
        pass

streak = 0
current_day = today

while daily_count.get(current_day, 0) >= st.session_state.daily_goal:
    streak += 1
    current_day -= timedelta(days=1)

# =========================
# UI
# =========================
if st.session_state.daily_goal > 0:
    progress = min(completed_sessions / st.session_state.daily_goal, 1.0)
else:
    progress = 0

st.subheader("Daily Goal")
st.write(f"{completed_sessions} / {st.session_state.daily_goal}")
st.progress(progress)

col1, col2 = st.columns(2)

with col1:
    st.metric("Focus Time", f"{total_focus_time} min")

with col2:
    st.metric("🔥 Streak", streak)

st.subheader("Session History")
st.write(st.session_state.history)

st.subheader("Database Sessions")
st.write(sessions)

