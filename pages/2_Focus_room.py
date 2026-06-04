import streamlit as st
from styles import *

st.markdown(f"""
<style>

/* app background */
.stApp {{
    background-color: {BACKGROUND};
    color: {TEXT};
}}

/* remove default padding feeling */
.block-container {{
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}}

/* metric card modernize */
div[data-testid="metric-container"] {{
    background: {CARD};
    border: 1px solid #1F2937;
    padding: 14px;
    border-radius: 14px;
}}

/* hide ugly headers spacing */
h3 {{
    color: {TEXT};
    font-weight: 600;
}}

/* dataframe styling */
[data-testid="stDataFrame"] {{
    border-radius: 12px;
    overflow: hidden;
}}

</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="PAUSE",
    page_icon="assets/logo.png",
    layout="wide"
)

# =========================
# FOCUS ROOM STATE
# =========================
if "rooms" not in st.session_state:
    st.session_state.rooms = {}

if "current_room" not in st.session_state:
    st.session_state.current_room = None

if "username" not in st.session_state:
    st.session_state.username = "Alex"

if "active_room" not in st.session_state:
    st.session_state.active_room = None

if "history" not in st.session_state:
    st.session_state.history = []

if "friends" not in st.session_state:
    st.session_state.friends = {
        "Bob": {
            "status": "online",
            "room": "Math Room",
            "mode": "Focus",
            "duration": 25
        },
        "Amy": {
            "status": "idle",
            "room": None,
            "mode": None,
            "duration": 0
        },
        "Carol": {
            "status": "offline",
            "room": None,
            "mode": None,
            "duration": 0
        }
    }

room = {
    "name": "Math Room",
    "mode": "focus",   # focus / discussion
    "members": [],
    "mic": False,
    "audio": False,
    "chat": False,
    "owner": "user123",
}

import streamlit as st

# =========================
# FRIEND LIST LAYOUT
# =========================
def render_friend_list():

    friends = st.session_state.friends
    rooms = st.session_state.rooms

    for name, info in friends.items():

        in_room = None
        room_id_found = None

        for rid, room in rooms.items():
            if name in room["members"]:
                in_room = room["name"]
                room_id_found = rid
                break

        status = info["status"]

        status_label = {
            "online": "Online",
            "idle": "Idle",
            "offline": "Offline"
        }.get(status, "Offline")

        left, right = st.columns([1.6, 2.4], gap="small", vertical_alignment="center")

        with left:
            st.markdown(
                f"<div style='display:flex; align-items:center;'>"
                f"<b>{name}</b>"
                f"<span style='margin-left:8px; color:#888; font-size:12px;'>({status_label})</span>"
                f"</div>",
                unsafe_allow_html=True
            )

        with right:
            room_name = info.get("room")
            if room_name:
                duration = info.get("duration", 0)
                st.markdown(
                    f"""
                    <div style="
                        display:flex;
                        align-items:center;
                        height:100%;
                        font-weight:500;
                    ">
                        <span style="color:#2ecc71; margin-right:6px;">LIVE</span>
                        · In Room ({room_name}) · {duration} min
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.markdown(
                    """
                    <div style="
                        display:flex;
                        align-items:center;
                        height:100%;
                        color:#888;
                    ">
                        Not in room
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown(
            "<div style='margin:4px 0; border-top:1px solid #eee;'></div>",
            unsafe_allow_html=True
        )

# =========================
# CREATE ROOM
# =========================
st.subheader("Create Room")

room_name = st.text_input(
    "Room ID",
    key="create_room_input"
)

room_ids = [
    rid for rid, r in st.session_state.rooms.items()
    if st.session_state.username in r["members"]
]

if st.session_state.current_room not in room_ids:
    st.session_state.current_room = None

room_mode = st.selectbox(
    "Room Mode",
    ["Focus Mode", "Discussion Mode"]
)
st.caption("🎯 Focus Mode: deep work, minimal interaction     💬 Discussion Mode: collaboration, full interaction")

if st.button("Create Room"):

    room_id = f"ROOM{len(st.session_state.rooms)+1}"

    st.session_state.rooms[room_id] = {
        "name": room_name,
        "mode": room_mode,
        "members": [st.session_state.username]
    }

    st.session_state.active_room = room_id
    st.session_state.current_room = room_id
    st.session_state.in_room = True

# =========================
# JOIN ROOM
# =========================
st.subheader("Join Room")

join_room_id = st.text_input(
    "Room ID",
    key="join_room_input"
)

if st.button("Join Room"):

    if join_room_id in st.session_state.rooms:

        room = st.session_state.rooms[join_room_id]

        if st.session_state.username not in room["members"]:
            room["members"].append(
                st.session_state.username
            )

        st.session_state.current_room = join_room_id

# =========================
# SHOW FRIEND LIST
# =========================
st.divider()
st.title("🧑‍🤝‍🧑 Friends (Global Status)")
render_friend_list()
st.divider()

# =========================
# ROOM DASHBOARD (CLEAN VERSION)
# =========================

st.title("💬 Focus Room")

col1, col2 = st.columns([1, 2])

# =========================
# LEFT SIDE - ROOM SELECT (PURE)
# =========================
with col1:

    st.subheader("Rooms List")
    room_ids = [
        rid for rid, r in st.session_state.rooms.items()
        if st.session_state.username in r["members"]
    ]
    if len(room_ids) == 0:
        st.info("No rooms yet")

    else:
        default_room = (
            st.session_state.active_room
            if st.session_state.active_room in room_ids
            else room_ids[0]
        )
        index = room_ids.index(default_room)
        selected_room = st.selectbox(
            "Select Room",
            room_ids,
            index=index,
            format_func=lambda x: st.session_state.rooms[x]["name"]
        )
        st.session_state.current_room = selected_room

# =========================
# RIGHT SIDE - ROOM DETAIL
# =========================
with col2:
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-child(2){
        border-left: 1px solid #eee;
        border-right: 1px solid #eee;
        padding-left: 10px;
        padding-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("")
    if st.session_state.current_room is None:
        st.caption("Select a room to view its details")
    else:
        room = st.session_state.rooms[st.session_state.current_room]

        # =========================
        # SIMPLE DETAIL DISPLAY
        # =========================
        st.markdown("### " + room["name"])
        st.write("**Mode:**", room["mode"])
        st.write("**Members:**", len(room["members"]))

        st.divider()

        # =========================
        # ACTIONS
        # =========================

        colA, colB = st.columns(2)

        with colA:
            if st.button("Enter Room"):
                if st.session_state.current_room is None:
                    st.warning("Please select a room first")
                    st.stop()
                room_id = st.session_state.current_room
                if room_id in st.session_state.rooms:
                    st.session_state.active_room = room_id
                    st.success(
                        f"Entered {st.session_state.rooms[room_id]['name']}"
                    )
                    st.rerun()

        with colB:
            if st.button("Leave Room"):
                room_id = st.session_state.active_room
                if room_id and room_id in st.session_state.rooms:
                    room_obj = st.session_state.rooms[room_id]
                    room_obj["members"] = [
                        m for m in room_obj["members"]
                        if m != st.session_state.username
                    ]
                st.session_state.active_room = None
                st.session_state.current_room = None
                st.rerun()

# st.subheader("🧑‍🤝‍🧑 Room Roster")

# for name in room["members"]:

#     info = st.session_state.friends.get(name, {
#         "status": "offline",
#         "room": None,
#         "duration": 0
#     })

#     status = info.get("status", "offline")
#     duration = info.get("duration", 0)
#     room_name = info.get("room")

#     # =========================
#     # LEFT: name + status
#     # =========================
#     left, right = st.columns([1.5, 2.5], gap="small")

#     with left:
#         status_label = {
#             "focusing": "LIVE",
#             "online": "Online",
#             "idle": "Idle",
#             "offline": "Offline"
#         }.get(status, "Offline")

#         st.markdown(
#             f"**{name}** ({status_label})"
#         )

#     # =========================
#     # RIGHT: activity
#     # =========================
#     with right:

#         if status == "focusing":
#             st.markdown(
#                 f"<span style='color:#2ecc71;'>LIVE</span> · Focusing for {duration} min",
#                 unsafe_allow_html=True
#             )

#         else:
#             st.markdown(
#                 "<span style='color:#888;'>Not active</span>",
#                 unsafe_allow_html=True
#             )

#     st.markdown("<div style='margin:3px 0; border-top:1px solid #eee;'></div>",
#                 unsafe_allow_html=True)