import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime
from supabase import create_client, Client

# Configure the page
st.set_page_config(page_title="System: Winter Arc", page_icon="🗡️", layout="wide")

# --- SUPABASE CONNECTION SETUP ---
SUPABASE_URL = "https://hhutdleywbpcwexgqupw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhodXRkbGV5d2JwY3dleGdxdXB3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA3NzE2MDEsImV4cCI6MjEwNjM0NzYwMX0.Vb6HEGAmSMfry9tTcHyiNDgMy5HKBmvttn_IYBv2BfY"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

@st.cache_resource
def authenticate_user():
    try:
        res = supabase.auth.sign_in_with_password({
            "email": "yuvateja1111369@gmail.com",
            "password": "YUVATEJA"
        })
        return res.user.id
    except Exception as e:
        return None

user_id = authenticate_user()

# --- ROAMING 3D IGRIS COMPANION CSS & JS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');

    html, body {
        height: 100vh;
        overflow: hidden !important;
        font-family: 'Rajdhani', sans-serif !important;
        color: #00e5ff !important;
        background-color: #05050a !important;
    }

    @keyframes slideShow {
        0% { background-image: linear-gradient(rgba(5, 5, 10, 0.25), rgba(5, 5, 10, 0.35)), url('https://raw.githubusercontent.com/yuvateja1111369-ai/winter-arc-tracker/main/bg1.jpg.jpg'); }
        25% { background-image: linear-gradient(rgba(5, 5, 10, 0.25), rgba(5, 5, 10, 0.35)), url('https://raw.githubusercontent.com/yuvateja1111369-ai/winter-arc-tracker/main/bg3.jpg.jpg'); }
        50% { background-image: linear-gradient(rgba(5, 5, 10, 0.25), rgba(5, 5, 10, 0.35)), url('https://raw.githubusercontent.com/yuvateja1111369-ai/winter-arc-tracker/main/bg4.jpg.jpg'); }
        75% { background-image: linear-gradient(rgba(5, 5, 10, 0.25), rgba(5, 5, 10, 0.35)), url('https://raw.githubusercontent.com/yuvateja1111369-ai/winter-arc-tracker/main/bg5.jpg.jpg'); }
        100% { background-image: linear-gradient(rgba(5, 5, 10, 0.25), rgba(5, 5, 10, 0.35)), url('https://raw.githubusercontent.com/yuvateja1111369-ai/winter-arc-tracker/main/bg1.jpg.jpg'); }
    }

    .stApp {
        background-size: contain !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        animation: slideShow 900s infinite;
        height: 100vh !important;
        overflow-y: auto !important;
        background-color: #05050a !important;
    }

    /* --- ROAMING 3D IGRIS WIDGET --- */
    #roaming-igris {
        position: fixed;
        width: 100px;
        height: 100px;
        z-index: 999999;
        pointer-events: none;
        transition: transform 0.1s ease-out;
        will-change: left, top, transform;
    }

    .igris-avatar {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #00e5ff;
        box-shadow: 0 0 20px #00e5ff, inset 0 0 10px #8a2be2;
        background-color: #000;
    }

    .igris-bubble {
        position: absolute;
        bottom: 95px;
        left: -20px;
        background: rgba(5, 5, 10, 0.9);
        border: 1px solid #00e5ff;
        color: #00e5ff;
        padding: 4px 8px;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
        white-space: nowrap;
    }

    h1 {
        text-align: center;
        text-transform: uppercase;
        color: #ffffff !important;
        text-shadow: 0 0 10px #00e5ff, 0 0 20px #00e5ff, 0 0 40px #8a2be2;
        animation: glow 2s infinite alternate;
        font-size: calc(1.5rem + 1vw);
    }

    @keyframes glow {
        from { text-shadow: 0 0 10px #00e5ff, 0 0 20px #00e5ff, 0 0 30px #8a2be2; }
        to { text-shadow: 0 0 20px #00e5ff, 0 0 30px #00e5ff, 0 0 50px #8a2be2; }
    }

    h2, h3 {
        color: #a200ff !important;
        border-bottom: 1px solid #00e5ff;
        padding-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .stButton>button {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: #00e5ff !important;
        border: 1px solid #00e5ff !important;
        border-radius: 0px !important;
        transition: 0.3s;
        text-transform: uppercase;
        font-weight: bold;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #00e5ff !important;
        color: #000000 !important;
        box-shadow: 0 0 15px #00e5ff;
    }
</style>

<!-- Roaming 3D Igris DOM Element -->
<div id="roaming-igris">
    <div class="igris-bubble" id="igris-text">"My Liege is watching..."</div>
    <img src="https://raw.githubusercontent.com/yuvateja1111369-ai/winter-arc-tracker/main/companion.png.jpeg" class="igris-avatar" alt="Igris">
</div>

<script>
    // JavaScript Roaming & 3D Tilt Engine for Igris
    const igris = document.getElementById('roaming-igris');
    const bubble = document.getElementById('igris-text');

    let posX = window.innerWidth - 150;
    let posY = window.innerHeight - 150;
    let targetX = posX;
    let targetY = posY;
    
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;

    // Track mouse position smoothly
    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Periodically pick a new random spot on screen for Igris to roam to
    setInterval(() => {
        targetX = Math.random() * (window.innerWidth - 150) + 50;
        targetY = Math.random() * (window.innerHeight - 200) + 50;
        
        const quotes = [
            "\"My Liege, fulfill your quests!\"",
            "\"Penalty quest avoided? Good.\"",
            "\"Shadow monarch's domain.\"",
            "\"Discipline is absolute.\""
        ];
        bubble.innerText = quotes[Math.floor(Math.random() * quotes.length)];
    }, 6000);

    // Animation loop for smooth roaming and 3D tilting toward the mouse cursor
    function roamLoop() {
        // Smooth glide toward target destination
        posX += (targetX - posX) * 0.03;
        posY += (targetY - posY) * 0.03;

        // Calculate 3D tilt based on mouse relative to Igris position
        let dx = mouseX - posX;
        let dy = mouseY - posY;
        let tiltX = (dy / window.innerHeight) * 30;
        let tiltY = (dx / window.innerWidth) * -30;

        igris.style.left = posX + 'px';
        igris.style.top = posY + 'px';
        igris.style.transform = `perspective(600px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale(1.05)`;

        requestAnimationFrame(roamLoop);
    }
    roamLoop();

    // React when any button is clicked on screen
    document.addEventListener('click', (e) => {
        if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
            bubble.innerText = "\"Quest action registered!\"";
            igris.style.transform += " scale(1.2)";
            setTimeout(() => {
                igris.style.transform = "scale(1)";
            }, 300);
        }
    });
</script>
""", unsafe_allow_html=True)

st.title("🗡 SYSTEM: PLAYER AWAKENING")
st.markdown("<p style='text-align: center; font-size: 18px; color: #a200ff;'>[ SYSTEM ACTIVE: OCT 1, 2026 – DEC 31, 2026 ]</p>", unsafe_allow_html=True)
st.divider()

LOCKED_RULES = [
    "WORK OUT 5-6 TIMES A WEEK", "DRINK 1 GALLON OF WATER DAILY", 
    "GET 8 HOURS OF SLEEP DAILY", "MAX OUT YOUR PROTEIN DAILY", 
    "READ 10 PAGES DAILY", "COLD SHOWERS DAILY", "10K STEPS DAILY", 
    "WAKE UP BY 5 AM", "NO EXCUSES", "NOTHING BUT 90 DAYS OF PURE DISCIPLINE"
]

date_range = pd.date_range(start="2026-10-01", end="2026-12-31")
days = [d.strftime("%b %d") for d in date_range]

# --- LOAD HABITS & PROGRESS FROM SUPABASE ---
if "tracker_df" not in st.session_state:
    initial_habits = [
        "WORK OUT 5-6 TIMES A WEEK", "DRINK 1 GALLON OF WATER DAILY", 
        "GET 8 HOURS OF SLEEP DAILY", "MAX OUT YOUR PROTEIN DAILY", 
        "READ 10 PAGES DAILY", "COLD SHOWERS DAILY", "10K STEPS DAILY", 
        "NO FAST FOOD", "NO SUGAR", "NO ALCOHOL", "NO DISTRACTIONS", 
        "WAKE UP BY 5 AM", "GO TO SLEEP BY 8 PM", "FOCUS ON YOURSELF", 
        "NO EXCUSES", "NOTHING BUT 90 DAYS OF PURE DISCIPLINE"
    ]
    
    loaded_habits = []
    progress_map = {}
    if user_id:
        try:
            res = supabase.table("habits").select("name, progress_json").eq("user_id", user_id).execute()
            if res.data:
                for row in res.data:
                    h_name = row["name"]
                    if not h_name.startswith("SLEEP_"):
                        loaded_habits.append(h_name)
                        if row.get("progress_json"):
                            progress_map[h_name] = json.loads(row["progress_json"])
        except Exception:
            pass
            
    habits_list = loaded_habits if loaded_habits else initial_habits
    
    grid_data = {}
    for day in days:
        day_vals = []
        for h in habits_list:
            day_vals.append(progress_map.get(h, {}).get(day, False))
        grid_data[day] = day_vals
        
    df = pd.DataFrame(grid_data)
    df.insert(0, "Habit Name", habits_list)
    st.session_state.tracker_df = df

# --- LOAD SLEEP RECORDS FROM SUPABASE HABITS TABLE ---
if "sleep_df" not in st.session_state:
    sleep_rows = ["10 hrs", "8 hrs", "6 hrs", "4 hrs", "2 hrs"]
    loaded_sleep = {}
    if user_id:
        try:
            res = supabase.table("habits").select("name, progress_json").eq("user_id", user_id).execute()
            if res.data:
                for row in res.data:
                    h_name = row["name"]
                    if h_name.startswith("SLEEP_"):
                        s_hours = h_name.replace("SLEEP_", "")
                        if row.get("progress_json"):
                            loaded_sleep[s_hours] = json.loads(row["progress_json"])
        except Exception:
            pass
            
    sleep_data = {}
    for day in days:
        day_vals = []
        for row_name in sleep_rows:
            day_vals.append(loaded_sleep.get(row_name, {}).get(day, False))
        sleep_data[day] = day_vals
        
    sleep_df = pd.DataFrame(sleep_data)
    sleep_df.insert(0, "Sleep Hours", sleep_rows)
    st.session_state.sleep_df = sleep_df

# --- SAVE BUTTON & CONTROLS HEADER ---
save_col1, save_col2 = st.columns([3, 1])
with save_col2:
    save_clicked = st.button("💾 SAVE PROGRESS", use_container_width=True)

# --- HABITS SECTION ---
st.subheader("STATUS: PENALTY QUEST EVASION")

col1, col2 = st.columns(2)
with col1:
    with st.form("add_habit_form", clear_on_submit=True):
        new_habit = st.text_input("➕ ADD NEW PARAMETER:")
        add_submitted = st.form_submit_button("ACCEPT QUEST")
        if add_submitted and new_habit:
            if new_habit not in st.session_state.tracker_df["Habit Name"].values:
                new_row = {"Habit Name": new_habit}
                for day in days:
                    new_row[day] = False
                new_df = pd.DataFrame([new_row])
                st.session_state.tracker_df = pd.concat([st.session_state.tracker_df, new_df], ignore_index=True)
                
                if user_id:
                    try:
                        supabase.table("habits").insert({"user_id": user_id, "name": new_habit, "progress_json": "{}"}).execute()
                    except Exception as err:
                        st.error(f"Cloud sync error: {err}")
                st.success(f"Added: {new_habit}!")
                st.rerun()

with col2:
    with st.form("remove_habit_form"):
        current_habits = st.session_state.tracker_df["Habit Name"].tolist()
        removable_habits = [h for h in current_habits if h not in LOCKED_RULES]
        habit_to_remove = st.selectbox("🗑 ABANDON QUEST:", options=[""] + removable_habits)
        remove_submitted = st.form_submit_button("DELETE")
        if remove_submitted and habit_to_remove:
            st.session_state.tracker_df = st.session_state.tracker_df[st.session_state.tracker_df["Habit Name"] != habit_to_remove]
            if user_id:
                try:
                    supabase.table("habits").delete().eq("user_id", user_id).eq("name", habit_to_remove).execute()
                except Exception:
                    pass
            st.rerun()

st.session_state.tracker_df["Completion Rate"] = (st.session_state.tracker_df[days].sum(axis=1) / len(days)) * 100
cols = ["Habit Name", "Completion Rate"] + days
st.session_state.tracker_df = st.session_state.tracker_df[cols]

edited_df = st.data_editor(
    st.session_state.tracker_df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Habit Name": st.column_config.Column(disabled=True),
        "Completion Rate": st.column_config.ProgressColumn(
            "COMPLETION %",
            help="Current Level",
            format="%d%%",
            min_value=0,
            max_value=100,
        )
    }
)

st.session_state.tracker_df = edited_df

# --- SLEEP SECTION ---
st.subheader("🌙 FATIGUE RECOVERY")
edited_sleep_df = st.data_editor(
    st.session_state.sleep_df,
    hide_index=True,
    use_container_width=True,
    column_config={"Sleep Hours": st.column_config.Column(disabled=True)}
)
st.session_state.sleep_df = edited_sleep_df

# --- HANDLE MANUAL SAVE BUTTON CLICK ---
if save_clicked and user_id:
    try:
        for _, row in st.session_state.tracker_df.iterrows():
            habit_name = row["Habit Name"]
            day_dict = {day: bool(row[day]) for day in days}
            
            existing = supabase.table("habits").select("name").eq("user_id", user_id).eq("name", habit_name).execute()
            if existing.data:
                supabase.table("habits").update({"progress_json": json.dumps(day_dict)}).eq("user_id", user_id).eq("name", habit_name).execute()
            else:
                supabase.table("habits").insert({"user_id": user_id, "name": habit_name, "progress_json": json.dumps(day_dict)}).execute()
            
        for _, row in st.session_state.sleep_df.iterrows():
            sleep_hours = row["Sleep Hours"]
            db_name = f"SLEEP_{sleep_hours}"
            day_dict = {day: bool(row[day]) for day in days}
            
            existing = supabase.table("habits").select("name").eq("user_id", user_id).eq("name", db_name).execute()
            if existing.data:
                supabase.table("habits").update({"progress_json": json.dumps(day_dict)}).eq("user_id", user_id).eq("name", db_name).execute()
            else:
                supabase.table("habits").insert({"user_id": user_id, "name": db_name, "progress_json": json.dumps(day_dict)}).execute()
            
        st.success("⚡ ALL PROGRESS & FATIGUE RECOVERY LOCKED IN CLOUD!")
    except Exception as e:
        st.error(f"Save failed: {e}")

# --- INTERACTIVE LIVE CHART ---
st.subheader("📈 PLAYER MOMENTUM")
daily_totals = st.session_state.tracker_df[days].sum()

fig = px.line(
    x=daily_totals.index, 
    y=daily_totals.values, 
    markers=True,
    labels={"x": "DATE", "y": "QUESTS COMPLETED"}
)

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#00e5ff",
    hovermode="x unified",
    xaxis=dict(showgrid=False, title_font=dict(size=14, family="Rajdhani"), tickfont=dict(family="Rajdhani")),
    yaxis=dict(showgrid=True, gridcolor="#1a1a2e", title_font=dict(size=14, family="Rajdhani"), tickfont=dict(family="Rajdhani"))
)

fig.update_traces(
    line=dict(color="#00e5ff", width=3), 
    marker=dict(size=10, color="#a200ff", line=dict(width=2, color="#00e5ff")),
    hovertemplate="%{x}<br>Completed: %{y}<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)
