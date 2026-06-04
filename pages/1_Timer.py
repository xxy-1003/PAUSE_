import streamlit as st
import time
import base64
from datetime import datetime
from storage import init_db, save_session, get_sessions
from styles import *

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="PAUSE Timer", layout="centered")

st.set_page_config(
    page_title="PAUSE",
    page_icon="assets/logo.png",
    layout="wide"
)

st.markdown(f"""
<style>
    .stApp {{
        background-color: {BACKGROUND};
        color: {TEXT};
    }}
</style>
""", unsafe_allow_html=True)

# =========================
# STATE
# =========================
if "mode" not in st.session_state:
    st.session_state.mode = "focus"

if "focus_minutes" not in st.session_state:
    st.session_state.focus_minutes = 30

if "recovery_minutes" not in st.session_state:
    st.session_state.recovery_minutes = 10

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = 5

if "interval_freq" not in st.session_state:
    st.session_state.interval_freq = 10   # minutes

if "interval_minutes" not in st.session_state:
    st.session_state.interval_minutes = 5  # minutes

if "running" not in st.session_state:
    st.session_state.running = False

if "focus_start" not in st.session_state:
    st.session_state.focus_start = None

if "focus_acc" not in st.session_state:
    st.session_state.focus_acc = 0

if "interval_start" not in st.session_state:
    st.session_state.interval_start = None

if "interval_acc" not in st.session_state:
    st.session_state.interval_acc = 0

if "next_interval" not in st.session_state:
    st.session_state.next_interval = st.session_state.interval_freq * 60

if "recovery_start" not in st.session_state:
    st.session_state.recovery_start = None

if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# AUDIO SYSTEM
# =========================
def play_sound(event, sound_source=None):
    try:
        if sound_source is None:
            st.toast(f"🔊 {event}")
            return

        if isinstance(sound_source, str):
            with open(sound_source, "rb") as f:
                audio_bytes = f.read()
        else:
            audio_bytes = sound_source.read()

        b64 = base64.b64encode(audio_bytes).decode()

        st.markdown(f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)

    except:
        st.toast(f"🔊 {event}")


# =========================
# INIT
# =========================
st.title("Timer")
init_db()
now = time.time()


# =========================
# SIDEBAR SETTINGS
# =========================
with st.sidebar:
    st.header("Settings")

    st.session_state.focus_minutes = st.number_input(
        "Focus Duration (min)",
        min_value=1,
        max_value=120,
        value=st.session_state.focus_minutes
    )

    st.session_state.recovery_minutes = st.number_input(
        "Recovery Duration (min)",
        min_value=1,
        max_value=60,
        value=st.session_state.recovery_minutes
    )

    st.session_state.daily_goal = st.number_input(
        "Daily Goal",
        min_value=1,
        max_value=20,
        value=st.session_state.daily_goal
    )

    st.session_state.interval_freq = st.number_input(
        "Interval Frequency (min)",
        min_value=1,
        max_value=60,
        value=st.session_state.interval_freq
    )

    st.session_state.interval_minutes = st.number_input(
        "Interval Break Duration (min)",
        min_value=1,
        max_value=30,
        value=st.session_state.interval_minutes
    )

    # =========================
    # AUDIO SYSTEM
    # =========================
    st.subheader("🔊 Ringtone System")

    sound_mode = st.radio("Sound Mode", ["Built-in", "Custom Upload"])

    builtin_sounds = {
        "Classic Bell": "assets/ringtone/classicBell.mp3",
        "Digital Beep": "assets/ringtone/digitalBeep.mp3",
        "Nature Sound": "assets/ringtone/natureSound.mp3",
        "Soft Chimes": "assets/ringtone/softChimes.mp3",
        "Zen Bell": "assets/ringtone/zenBell.mp3"
    }

    selected_sound = None

    if sound_mode == "Built-in":
        sound_name = st.selectbox("Choose Sound", list(builtin_sounds.keys()))
        selected_sound = builtin_sounds[sound_name]
    else:
        selected_sound = st.file_uploader("Upload sound", type=["mp3", "wav"])

    # AUDIO PREVIEW
    st.subheader("🔊 Preview")
    if st.button("▶️ Play Preview"):
        play_sound("Preview", selected_sound)


# =========================
# CONSTANTS
# =========================
FOCUS_DURATION = st.session_state.focus_minutes * 60
RECOVERY_DURATION = st.session_state.recovery_minutes * 60
INTERVAL_FREQ = st.session_state.interval_freq * 60
INTERVAL_DURATION = st.session_state.interval_minutes * 60

# =========================
# TIME ENGINE
# =========================
focus_elapsed = 0
interval_elapsed = 0

if st.session_state.focus_start:
    focus_elapsed = st.session_state.focus_acc + (now - st.session_state.focus_start)
else:
    focus_elapsed = st.session_state.focus_acc

if st.session_state.interval_start:
    interval_elapsed = st.session_state.interval_acc + (now - st.session_state.interval_start)
else:
    interval_elapsed = st.session_state.interval_acc


def pause_focus():
    if st.session_state.focus_start:
        st.session_state.focus_acc += now - st.session_state.focus_start
        st.session_state.focus_start = None


def pause_interval():
    if st.session_state.interval_start:
        st.session_state.interval_acc += now - st.session_state.interval_start
        st.session_state.interval_start = None


def reset_interval():
    st.session_state.interval_start = None
    st.session_state.interval_acc = 0


def start_focus():
    st.session_state.mode = "focus"
    st.session_state.running = True

    if st.session_state.focus_start is None:
        st.session_state.focus_start = now

    st.session_state.next_interval = st.session_state.interval_freq * 60


# =========================
# UI
# =========================
if st.session_state.mode == "focus":
    limit = FOCUS_DURATION
    label = "Focus"
    elapsed = focus_elapsed

elif st.session_state.mode == "interval":
    limit = INTERVAL_DURATION
    label = "Interval"
    elapsed = interval_elapsed

elif st.session_state.mode == "recovery":
    limit = RECOVERY_DURATION
    label = "Recovery"
    start = st.session_state.recovery_start
    elapsed = (now - start) if start is not None else 0

elif st.session_state.mode == "pending_recovery":
    limit = 0
    label = "Finish"
    elapsed = 0

else:
    limit = FOCUS_DURATION
    label = "Focus"
    elapsed = 0


st.subheader(f" {label}")
st.metric("Time Left",
          f"{int(max(0, limit - elapsed))//60:02d}:{int(max(0, limit - elapsed))%60:02d}")


# =========================
# BUTTONS
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Start / Resume", use_container_width=True):
        start_focus()
        play_sound("Focus Start", selected_sound)
        st.rerun()

with col2:
    if st.button("Pause", use_container_width=True):
        pause_focus()
        pause_interval()
        st.session_state.running = False
        st.rerun()

with col3:
    if st.button("Reset", use_container_width=True):
        st.session_state.mode = "focus"
        st.session_state.running = False
        st.session_state.focus_start = None
        st.session_state.focus_acc = 0
        reset_interval()
        st.session_state.next_interval = st.session_state.interval_freq * 60
        st.rerun()

with col4:
    if st.button("Switch mode", use_container_width=True):
        if st.session_state.mode == "focus":
            st.session_state.mode = "recovery"
            st.session_state.time_left = recovery_minutes * 60

        else:
            st.session_state.mode = "focus"
            st.session_state.time_left = focus_minutes * 60

        st.rerun()

# =========================
# CORE ENGINE
# =========================
if st.session_state.mode == "focus" and st.session_state.running:

    if focus_elapsed >= st.session_state.next_interval and focus_elapsed < FOCUS_DURATION:
        pause_focus()

        st.session_state.mode = "interval"
        st.session_state.interval_start = now
        st.session_state.next_interval += INTERVAL_FREQ

        play_sound("Interval Start", selected_sound)
        st.rerun()

    if focus_elapsed >= FOCUS_DURATION:
        pause_focus()

        st.session_state.mode = "pending_recovery"

        save_session(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            focus_minutes,
            "FOCUS_COMPLETED"
        )

        st.session_state.history.append("focus_done")

        play_sound("Focus End", selected_sound)
        st.rerun()


# =========================
# INTERVAL END
# =========================
if st.session_state.mode == "interval":
    if interval_elapsed >= INTERVAL_DURATION:

        reset_interval()
        play_sound("Interval End", selected_sound)

        st.session_state.mode = "focus"
        st.session_state.focus_start = now
        st.session_state.running = True

        st.rerun()


# =========================
# RECOVERY
# =========================
if st.session_state.mode == "pending_recovery":

    st.warning("Focus finished. Enter recovery?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Recovery"):
            st.session_state.mode = "recovery"
            st.session_state.recovery_start = now
            play_sound("Recovery Start", selected_sound)
            st.rerun()

    with col2:
        if st.button("Skip"):
            start_focus()
            st.rerun()


if st.session_state.mode == "recovery":
    if st.session_state.recovery_start is None:
        pass
    else:
        if now - st.session_state.recovery_start >= RECOVERY_DURATION:

            # ✅ SAVE RECOVERY SESSION
            save_session(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                recovery_minutes,
                "RECOVERY_COMPLETED"
            )

            play_sound("Recovery End", selected_sound)
            start_focus()
            st.rerun()


# =========================
# AUTO REFRESH
# =========================
if "last_tick" not in st.session_state:
    st.session_state.last_tick = time.time()

if st.session_state.mode in ["focus", "interval", "recovery"]:
    if time.time() - st.session_state.last_tick >= 1:
        st.session_state.last_tick = time.time()
        st.rerun()

# =========================
# DAILY GOAL
# =========================
st.subheader("Daily Goal")

sessions = get_sessions()
today = datetime.now().strftime("%Y-%m-%d")

completed = len([
    s for s in sessions
    if "FOCUS_COMPLETED" in str(s)
    and today in str(s)
])

st.write(f"{completed} / {st.session_state.daily_goal}")
progress = completed / max(st.session_state.daily_goal, 1)
st.progress(min(progress, 1.0))


# # =========================
# # DEBUG
# # =========================
# st.subheader("Database")
# st.write(get_sessions())

# st.subheader("History")
# st.write(st.session_state.history)