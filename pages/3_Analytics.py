import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from storage import get_sessions
from datetime import datetime, timedelta
from styles import *

st.set_page_config(
    page_title="PAUSE",
    page_icon="assets/logo.png",
    layout="wide"
)

# =========================
# 🎨 STYLES
# =========================
st.title("📊 Analytics")

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

# =========================
# 📦 LOAD DATA
# =========================
sessions = get_sessions()

parsed = [
    {
        "date": datetime.strptime(s[0], "%Y-%m-%d %H:%M:%S"),
        "duration": s[1],
        "status": s[2]
    }
    for s in sessions
]

# =========================
# 📅 TODAY
# =========================
today = datetime.now().date()
yesterday = today - timedelta(days=1)

daily = [s for s in parsed if s["date"].date() == today]
yesterday_data = [s for s in parsed if s["date"].date() == yesterday]

daily_total = sum(s["duration"] for s in daily)
yesterday_total = sum(s["duration"] for s in yesterday_data)

hours = daily_total // 60
minutes = daily_total % 60

delta_focus = daily_total - yesterday_total

# =========================
# DAILY GOAL
# =========================
goal = st.session_state.get("daily_goal", 4)

# =========================
# STREAK (UNCHANGED LOGIC, SAFE)
# =========================
streak = 0
current_day = today

for i in range(30):

    day_sessions = [
        s for s in parsed
        if s["date"].date() == current_day
        and s["status"] in ["FOCUS_COMPLETED", "COMPLETED"]
    ]

    if len(day_sessions) >= goal:
        streak += 1
        current_day -= timedelta(days=1)
    else:
        break

# =========================
# UI
# =========================
st.subheader("📅 Today")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Focus Time",
        f"{hours}h {minutes}m",
        delta=f"{delta_focus:+} min vs yesterday"
    )

with col2:
    today_sessions = [
        s for s in daily
        if s["status"] in ["FOCUS_COMPLETED", "COMPLETED"]
    ]

    yesterday_sessions = [
        s for s in yesterday_data
        if s["status"] in ["FOCUS_COMPLETED", "COMPLETED"]
    ]

    st.metric(
        "Sessions",
        len(today_sessions),
        delta=len(today_sessions) - len(yesterday_sessions)
    )

with col3:
    st.metric(
        "🔥 Streak",
        streak,
        delta="Keep going" if streak > 0 else "Start today"
    )

# =========================
# PROGRESS
# =========================
progress = len(daily) / goal if goal > 0 else 0
st.progress(min(progress, 1.0))
st.caption(f"{len(daily)} / {goal} sessions")

# =========================
# 🧠 BURNOUT 
# =========================
this_week_start = datetime.now() - timedelta(days=7)

this_week = [
    s for s in parsed
    if s["date"] >= this_week_start
]

# focus ONLY completed
this_focus = sum(
    s["duration"] for s in this_week
    if s["status"] in ["COMPLETED", "FOCUS_COMPLETED"]
)

# recovery ONLY real DB breaks
this_break = [
    s for s in this_week
    if s["status"] == "BREAK_COMPLETED"
]

recovery_time = sum(s["duration"] for s in this_break)

total_load = this_focus + recovery_time

burnout_ratio = this_focus / total_load if total_load else 0
burnout_pct = int(burnout_ratio * 100)

# =========================
# LEVEL
# =========================
if burnout_pct >= 75:
    level = "🔥 High Risk"
elif burnout_pct >= 50:
    level = "⚠️ Medium"
else:
    level = "🟢 Healthy"

st.subheader("🧠 Burnout")
st.caption(
    "Based on your focus and recovery activity over the past 7 days."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Level", level)

with col2:
    st.metric("Focus", f"{this_focus} min")

with col3:
    st.metric("Recovery", f"{recovery_time} min")

st.metric("Workload Pressure", f"{burnout_pct}%")

# =========================
# INSIGHT
# =========================
if burnout_pct >= 75:
    pressure_insight = "High workload pressure detected — consider reducing focus load."
elif burnout_pct >= 50:
    pressure_insight = "Moderate workload balance — keep monitoring."
else:
    pressure_insight = "Healthy balance — workload is well managed."

if burnout_pct >= 75:
    bg_color = "#FEE2E2"
    text_color = "#B91C1C"

elif burnout_pct >= 50:
    bg_color = "#FEF3C7"
    text_color = "#92400E"

else:
    bg_color = "#DCFCE7"
    text_color = "#166534"

st.markdown(f"""
<div style="
    margin-top:20px;
    margin-bottom:20px;
    padding:14px;
    border-radius:12px;
    background:{bg_color};
    color:{text_color};
    font-size:14px;
    line-height:1.5;
">
💡 {pressure_insight}
</div>
""", unsafe_allow_html=True)

# =========================
# VISUAL BAR
# =========================
st.markdown(
    """
    <div style="
        display:flex;
        justify-content:space-between;
        font-size:13px;
        color:#9CA3AF;
        margin-bottom:6px;
    ">
        <div>Recovery</div>
        <div>Focus</div>
    </div>
    """,
    unsafe_allow_html=True
)

def burnout_bar(focus, recovery):

    total = focus + recovery

    if total == 0:
        total = 1

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[recovery],
        y=[""],
        orientation="h",
        marker=dict(color="#34D399", line=dict(width=0)),
        showlegend=False,
        hovertemplate="Recovery: %{x} min<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        x=[focus],
        y=[""],
        orientation="h",
        marker=dict(color="#60A5FA", line=dict(width=0)),
        showlegend=False,
        hovertemplate="Focus: %{x} min<extra></extra>"
    ))

    fig.update_layout(
        barmode="stack",
        height=40,
        margin=dict(l=0, r=0, t=0, b=0),

        xaxis=dict(
            visible=False,
            range=[0, total], 
            zeroline=False,
            showgrid=False
        ),

        yaxis=dict(
            visible=False,
            zeroline=False,
            showgrid=False
        ),

        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",

        bargap=0,
        bargroupgap=0
    )

    return fig

st.plotly_chart(burnout_bar(this_focus, recovery_time), use_container_width=True)

# =========================
# WEEKLY TREND
# =========================
week_start = datetime.now() - timedelta(days=7)

week_data = [
    s for s in parsed
    if s["date"] >= week_start
]

daily_map = {}

for s in week_data:
    day = s["date"].strftime("%a")
    daily_map[day] = daily_map.get(day, 0) + s["duration"]

order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

trend_data = [{"day": d, "focus": daily_map.get(d, 0)} for d in order]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[d["day"] for d in trend_data],
    y=[d["focus"] for d in trend_data],
    mode="lines+markers",
    line=dict(color="#60A5FA", width=3),
    marker=dict(size=6)
))

fig.update_layout(
    height=280,
    margin=dict(l=0, r=0, t=20, b=0),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# MULTI WEEK
# =========================
st.subheader("📆 Multi-week Comparison")

weeks_count = st.selectbox("Compare weeks", [2, 3, 4, 6])

weeks = []

for i in range(weeks_count):
    start = datetime.now() - timedelta(days=7*(i+1))
    end = datetime.now() - timedelta(days=7*i)

    week_sessions = [
        s for s in parsed
        if start <= s["date"] < end
    ]

    total = sum(s["duration"] for s in week_sessions)

    weeks.append({
        "week": f"W{weeks_count-i}\n{start.strftime('%b %d')} - {end.strftime('%b %d')}",
        "focus": total
    })

df = pd.DataFrame(weeks)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=df["week"],
    y=df["focus"],
    marker=dict(color="#34D399"),
    hovertemplate="%{x}<br>%{y} min<extra></extra>"
))

fig.update_layout(
    height=280,
    margin=dict(l=0, r=0, t=10, b=0),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig, use_container_width=True)