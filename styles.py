# =========================
# PAUSE UI DESIGN SYSTEM v1
# =========================

# 🎨 COLOR SYSTEM
PRIMARY = "#4F46E5"      # Indigo (focus)
SUCCESS = "#22C55E"      # completed
WARNING = "#F59E0B"      # break
DANGER = "#EF4444"       # stop/reset

BACKGROUND = "#0F172A"   # main background
CARD = "#111827"         # card surface
TEXT = "#E5E7EB"         # main text
MUTED = "#94A3B8"        # secondary text


# 🧱 CARD STYLE
CARD_STYLE = f"""
    background-color: {CARD};
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #1F2937;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
"""


# 🔘 BUTTON STYLES (HTML/CSS fallback if needed)
PRIMARY_BUTTON = f"""
    background-color: {PRIMARY};
    color: white;
    padding: 10px 18px;
    border-radius: 12px;
    border: none;
"""

SECONDARY_BUTTON = f"""
    background-color: transparent;
    color: {TEXT};
    border: 1px solid #334155;
    padding: 10px 18px;
    border-radius: 12px;
"""

DANGER_BUTTON = f"""
    background-color: {DANGER};
    color: white;
    padding: 10px 18px;
    border-radius: 12px;
    border: none;
"""


# 📊 STATUS COLORS MAP
STATUS_COLOR = {
    "focus": PRIMARY,
    "break": WARNING,
    "pause": MUTED,
    "done": SUCCESS,
    "stop": DANGER
}


# ⏱ TIMER CONFIG (UI ONLY)
TIMER_SIZE = 220  # px equivalent concept
TIMER_THICKNESS = 8


# 🧠 LAYOUT HELPERS
PAGE_PADDING = 24
CARD_GAP = 16
SECTION_GAP = 28