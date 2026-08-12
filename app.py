import streamlit as st
import time
import random
import pandas as pd
import numpy as np

# ----------------------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM CSS (Cyberpunk Design System)
# ----------------------------------------------------------------------
st.set_page_config(page_title="SNAKE // NEON TERMINAL", layout="wide")

CYBER_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=JetBrains+Mono:wght@400;600&display=swap');

/* ----- GLOBAL RESET & BASE ----- */
html, body, .stApp {
    background: #0a0a0f !important;
    color: #e0e0e0 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ----- SCANLINE OVERLAY (full page) ----- */
body::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.25) 2px,
        rgba(0,0,0,0.25) 4px
    );
    z-index: 9999;
}

/* ----- HEADINGS (Orbitron) ----- */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Orbitron', monospace !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #00ff88;
}

/* ----- GLITCH EFFECT ON MAIN TITLE ----- */
.glitch-title {
    display: inline-block;
    animation: glitch 3s infinite;
}
@keyframes glitch {
    0%, 100% { transform: translate(0); text-shadow: -2px 0 #ff00ff, 2px 0 #00d4ff; }
    20% { transform: translate(-1px, 1px); text-shadow: -1px 0 #ff00ff, 3px 0 #00d4ff; }
    40% { transform: translate(1px, -1px); text-shadow: 2px 0 #ff00ff, -1px 0 #00d4ff; }
    60% { transform: translate(-1px, -1px); text-shadow: -2px 0 #ff00ff, 2px 0 #00d4ff; }
    80% { transform: translate(1px, 1px); text-shadow: 1px 0 #ff00ff, -1px 0 #00d4ff; }
}

/* ----- SIDEBAR (terminal panel) ----- */
section[data-testid="stSidebar"] {
    background: #12121a !important;
    border-right: 1px solid #2a2a3a;
    box-shadow: inset -1px 0 0 0 #2a2a3a;
}
section[data-testid="stSidebar"] .stSelectbox, 
section[data-testid="stSidebar"] .stColorPicker,
section[data-testid="stSidebar"] .stSlider {
    background: #1c1c2e !important;
    border: 1px solid #2a2a3a;
    clip-path: polygon(0 6px, 6px 0, calc(100% - 6px) 0, 100% 6px, 100% calc(100% - 6px), calc(100% - 6px) 100%, 6px 100%, 0 calc(100% - 6px));
    padding: 0.5rem;
    margin-bottom: 1rem;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stColorPicker label,
section[data-testid="stSidebar"] .stSlider label {
    color: #6b7280 !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 0.1em;
}

/* ----- BUTTONS (chamfered + neon) ----- */
.stButton button {
    background: transparent !important;
    border: 2px solid #00ff88 !important;
    color: #00ff88 !important;
    font-family: 'Share Tech Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    padding: 0.6rem 1.4rem;
    clip-path: polygon(0 8px, 8px 0, calc(100% - 8px) 0, 100% 8px, 100% calc(100% - 8px), calc(100% - 8px) 100%, 8px 100%, 0 calc(100% - 8px));
    transition: all 0.15s steps(4);
    box-shadow: 0 0 5px rgba(0,255,136,0.2);
}
.stButton button:hover {
    background: #00ff88 !important;
    color: #0a0a0f !important;
    box-shadow: 0 0 15px #00ff88, 0 0 30px rgba(0,255,136,0.3);
}
/* Secondary buttons (magenta) */
.stButton button.secondary {
    border-color: #ff00ff !important;
    color: #ff00ff !important;
}
.stButton button.secondary:hover {
    background: #ff00ff !important;
    color: #0a0a0f !important;
    box-shadow: 0 0 15px #ff00ff, 0 0 30px rgba(255,0,255,0.3);
}
/* Reset button – special glitch CTA */
.stButton button.reset {
    background: #00ff88 !important;
    color: #0a0a0f !important;
    border: 2px solid #00ff88 !important;
    box-shadow: 0 0 10px #00ff88, 0 0 20px rgba(0,255,136,0.5);
    animation: glitch 2s infinite;
}
.stButton button.reset:hover {
    filter: brightness(1.2);
    box-shadow: 0 0 20px #00ff88, 0 0 40px rgba(0,255,136,0.6);
}

/* ----- METRICS (neon cards) ----- */
div[data-testid="stMetric"] {
    background: #12121a;
    border: 1px solid #2a2a3a;
    clip-path: polygon(0 8px, 8px 0, calc(100% - 8px) 0, 100% 8px, 100% calc(100% - 8px), calc(100% - 8px) 100%, 8px 100%, 0 calc(100% - 8px));
    padding: 1rem 1.5rem;
    box-shadow: 0 0 10px rgba(0,255,136,0.1);
}
div[data-testid="stMetric"] label {
    color: #6b7280 !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 0.1em;
}
div[data-testid="stMetric"] div {
    color: #00ff88 !important;
    font-size: 2rem !important;
    text-shadow: 0 0 10px rgba(0,255,136,0.4);
}

/* ----- ALERTS (terminal style) ----- */
.stAlert {
    background: #12121a !important;
    border: 1px solid #2a2a3a !important;
    clip-path: polygon(0 6px, 6px 0, calc(100% - 6px) 0, 100% 6px, 100% calc(100% - 6px), calc(100% - 6px) 100%, 6px 100%, 0 calc(100% - 6px));
    padding: 1rem;
    font-family: 'Share Tech Mono', monospace;
    border-left: 4px solid #00ff88 !important;
}
.stAlert[data-baseweb="notification"] {
    border-left-color: #ff00ff !important;
}

/* ----- DATA FRAME (hacker terminal) ----- */
.stDataFrame {
    background: #0a0a0f !important;
    border: 1px solid #2a2a3a !important;
    clip-path: polygon(0 6px, 6px 0, calc(100% - 6px) 0, 100% 6px, 100% calc(100% - 6px), calc(100% - 6px) 100%, 6px 100%, 0 calc(100% - 6px));
}
.stDataFrame th {
    color: #00ff88 !important;
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    background: #1c1c2e !important;
}
.stDataFrame td {
    color: #e0e0e0 !important;
    font-family: 'JetBrains Mono', monospace;
}

/* ----- GRID CONTAINER (the game board) ----- */
.game-board {
    background: #0a0a0f;
    border: 1px solid #2a2a3a;
    clip-path: polygon(0 10px, 10px 0, calc(100% - 10px) 0, 100% 10px, 100% calc(100% - 10px), calc(100% - 10px) 100%, 10px 100%, 0 calc(100% - 10px));
    padding: 12px;
    box-shadow: 0 0 20px rgba(0,255,136,0.1);
}

/* ----- MISC ----- */
hr {
    border-color: #2a2a3a !important;
    box-shadow: 0 0 2px rgba(0,255,136,0.2);
}
"""

st.markdown(f"<style>{CYBER_CSS}</style>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 2. APP TITLE (with glitch effect)
# ----------------------------------------------------------------------
st.markdown(
    '<h1 class="glitch-title">⚡ MODERN AI‑POWERED SNAKE GAME</h1>',
    unsafe_allow_html=True
)

# ----------------------------------------------------------------------
# 3. SIDEBAR – ENVIRONMENT & SETTINGS
# ----------------------------------------------------------------------
st.sidebar.markdown("### 🎮 TERMINAL CONFIG")
environment = st.sidebar.selectbox(
    "SELECT ZONE",
    ["Futuristic Neon", "Retro Dark", "Desert Hazard"]
)
snake_color = st.sidebar.color_picker("SNAKE SKIN", "#00FF88")
base_speed = st.sidebar.slider(
    "BASE SPEED (lower = faster)",
    0.05, 0.4, 0.15, step=0.05
)

# Reset / Launch button (glitch style)
if st.sidebar.button("🚀 LAUNCH / RESET", key="reset_btn"):
    reset_game()

st.sidebar.markdown("---")
st.sidebar.caption("> SYSTEM v2.0 // NEON CORE")

# ----------------------------------------------------------------------
# 4. SESSION STATE INIT
# ----------------------------------------------------------------------
if 'snake' not in st.session_state:
    st.session_state.snake = [[10, 10], [10, 11], [10, 12]]
    st.session_state.direction = "UP"
    st.session_state.food = [random.randint(2, 17), random.randint(2, 17)]
    st.session_state.powerup = [random.randint(2, 17), random.randint(2, 17)]
    st.session_state.powerup_active = False
    st.session_state.powerup_timer = 0
    st.session_state.obstacle = [random.randint(3, 16), random.randint(3, 16)]
    st.session_state.obstacle_dir = 1
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_started = False
    st.session_state.logs = []

def reset_game():
    st.session_state.snake = [[10, 10], [10, 11], [10, 12]]
    st.session_state.direction = "UP"
    st.session_state.food = [random.randint(2, 17), random.randint(2, 17)]
    st.session_state.powerup = [random.randint(2, 17), random.randint(2, 17)]
    st.session_state.powerup_active = False
    st.session_state.powerup_timer = 0
    st.session_state.obstacle = [random.randint(3, 16), random.randint(3, 16)]
    st.session_state.obstacle_dir = 1
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_started = True

# ----------------------------------------------------------------------
# 5. CONTROL BUTTONS (direction)
# ----------------------------------------------------------------------
st.markdown("### 🕹️ DIRECTIVE INPUT")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⬅ LEFT", key="left") and st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
with col2:
    if st.button("⬆ UP", key="up") and st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
with col3:
    if st.button("⬇ DOWN", key="down") and st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"
with col4:
    if st.button("➡ RIGHT", key="right") and st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"

# ----------------------------------------------------------------------
# 6. GAME ENGINE (identical logic)
# ----------------------------------------------------------------------
grid_size = 20
current_speed = base_speed

if st.session_state.powerup_active:
    current_speed = base_speed + 0.80
    st.session_state.powerup_timer -= 1
    if st.session_state.powerup_timer <= 0:
        st.session_state.powerup_active = False

if st.session_state.game_started and not st.session_state.game_over:
    st.session_state.obstacle[1] += st.session_state.obstacle_dir
    if st.session_state.obstacle[1] >= grid_size - 2 or st.session_state.obstacle[1] <= 1:
        st.session_state.obstacle_dir *= -1

    head = st.session_state.snake[0].copy()
    if st.session_state.direction == "UP": head[0] -= 1
    elif st.session_state.direction == "DOWN": head[0] += 1
    elif st.session_state.direction == "LEFT": head[1] -= 1
    elif st.session_state.direction == "RIGHT": head[1] += 1

    if (head[0] < 0 or head[0] >= grid_size or head[1] < 0 or head[1] >= grid_size or 
        head in st.session_state.snake or head == st.session_state.obstacle):
        st.session_state.game_over = True
    else:
        st.session_state.snake.insert(0, head)
        if head == st.session_state.food:
            st.session_state.score += 10
            st.session_state.food = [random.randint(1, grid_size-2), random.randint(1, grid_size-2)]
        elif head == st.session_state.powerup:
            st.session_state.powerup_active = True
            st.session_state.powerup_timer = 20
            st.session_state.powerup = [random.randint(1, grid_size-2), random.randint(1, grid_size-2)]
        else:
            st.session_state.snake.pop()

    st.session_state.logs.append({
        "Head_X": head[0], "Head_Y": head[1], 
        "Target_X": st.session_state.food[0], "Target_Y": st.session_state.food[1],
        "Obstacle_X": st.session_state.obstacle[0], "Obstacle_Y": st.session_state.obstacle[1],
        "Score": st.session_state.score,
        "PowerUp_Active": st.session_state.powerup_active
    })

# ----------------------------------------------------------------------
# 7. VISUAL DISPLAY (game board + HUD)
# ----------------------------------------------------------------------
bg_color = "#050508" if environment == "Futuristic Neon" else ("black" if environment == "Retro Dark" else "#2b1d0c")

grid_html = f'<div class="game-board" style="grid-template-columns: repeat({grid_size}, 18px); display: grid; background-color: {bg_color}; width: fit-content; margin: auto;">'
for r in range(grid_size):
    for c in range(grid_size):
        current_pos = [r, c]
        if current_pos in st.session_state.snake:
            color = "#FFF" if current_pos == st.session_state.snake[0] else snake_color
            # Neon glow for snake
            grid_html += f'<div style="width: 16px; height: 16px; background-color: {color}; margin: 1px; border-radius: 2px; box-shadow: 0 0 6px {color};"></div>'
        elif current_pos == st.session_state.food:
            grid_html += '<div style="width: 16px; height: 16px; background-color: #ff3366; margin: 1px; border-radius: 50%; box-shadow: 0 0 12px #ff3366;"></div>'
        elif current_pos == st.session_state.powerup and not st.session_state.powerup_active:
            grid_html += '<div style="width: 16px; height: 16px; background-color: #00d4ff; margin: 1px; border-radius: 2px; box-shadow: 0 0 12px #00d4ff;"></div>'
        elif current_pos == st.session_state.obstacle:
            grid_html += '<div style="width: 16px; height: 16px; background-color: #ff00ff; margin: 1px; clip-path: polygon(50% 0%, 0% 100%, 100% 100%); box-shadow: 0 0 8px #ff00ff;"></div>'
        else:
            grid_html += '<div style="width: 16px; height: 16px; background-color: #1a1a24; margin: 1px; border-radius: 1px;"></div>'
grid_html += '</div>'

main_col, side_col = st.columns([2, 1])

with main_col:
    st.markdown(grid_html, unsafe_allow_html=True)
    # HUD metrics
    hud_col1, hud_col2 = st.columns(2)
    hud_col1.metric("SCORE", f"{st.session_state.score} PTS")
    hud_col2.metric("FPS", f"{round(1/current_speed, 1)}")
    
    if st.session_state.powerup_active:
        st.info(f"🛡️ TIME WARP ACTIVE – Speed stabilized. Remaining: {st.session_state.powerup_timer} frames.")
    if not st.session_state.game_started:
        st.warning("⚡ ENGINE OFFLINE – Click 'LAUNCH / RESET' on the sidebar.")
    elif st.session_state.game_over:
        st.error("🚨 CRITICAL COLLISION – Simulation terminated. Reset via sidebar.")

# ----------------------------------------------------------------------
# 8. NEURAL ANALYTICS PANEL
# ----------------------------------------------------------------------
with side_col:
    st.subheader("🤖 NEURAL COACH")
    if st.session_state.game_started and len(st.session_state.snake) > 0:
        head_now = st.session_state.snake[0]
        obs_now = st.session_state.obstacle
        
        st.markdown("---")
        st.markdown("**📡 HAZARD TELEMETRY**")
        distance_to_obstacle = abs(head_now[0] - obs_now[0]) + abs(head_now[1] - obs_now[1])
        
        if distance_to_obstacle <= 3:
            st.error(f"🚨 EVASIVE MANEUVER REQUIRED! Moving hazard is only {distance_to_obstacle} blocks away!")
        elif head_now[0] < 3 or head_now[0] > grid_size - 4 or head_now[1] < 3 or head_now[1] > grid_size - 4:
            st.warning("⚠️ WALL PROXIMITY – Core grid boundaries close. Plan turns.")
        else:
            st.success("🎯 OPTIMAL SECTOR – Area safe. Move towards the Target Core (Red dot).")

        if st.session_state.logs:
            st.markdown("**📊 DEEP LEARNING LOGS**")
            df = pd.DataFrame(st.session_state.logs[-4:])
            st.dataframe(df[["Head_X", "Head_Y", "Target_X", "Obstacle_X", "PowerUp_Active"]], use_container_width=True)
    else:
        st.info("Awaiting telemetry stream... Start game to feed neural network.")

# ----------------------------------------------------------------------
# 9. GAME LOOP (rerun)
# ----------------------------------------------------------------------
if st.session_state.game_started and not st.session_state.game_over:
    time.sleep(current_speed)
    st.rerun()
