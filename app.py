import streamlit as st
import pandas as pd
import plotly.express as px
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

# Auto-authenticate the test user for session persistence
@st.cache_resource
def authenticate_user():
    try:
        res = supabase.auth.sign_in_with_password({
            "email": "yuvateja1111369@gmail.com",
            "password": "YUVATEJA"
        })
        return res.user.id
    except Exception as e:
        st.error(f"System Authentication Failed: {e}")
        return None

user_id = authenticate_user()

# --- SOLO LEVELING CSS THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif !important;
        background-color: #0a0a0f !important;
        color: #00e5ff !important;
    }

    h1 {
        text-align: center;
        text-transform: uppercase;
        color: #ffffff !important;
        text-shadow: 0 0 10px #00e5ff, 0 0 20px #00e5ff, 0 0 40px #8a2be2;
        animation: glow 2s infinite alternate;
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
        background-color: transparent !important;
        color: #00e5ff !important;
        border: 1px solid #00e5ff !important;
        border-radius: 0px !important;
        transition: 0.3s;
        text-transform: uppercase;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background-color: #00e5ff !important;
        color: #000000 !important;
        box-shadow: 0 0 15px #00e5ff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🗡 SYSTEM: PLAYER AWAKENING")
st.markdown("<p style='text-align: center; font-size: 20px; color: #a200ff;'>[ CLOUD SYNC ACTIVE: 90 DAYS OF PURE DISCIPLINE ]</p>", unsafe_allow_html=True)
st.divider()

LOCKED_RULES = [
    "WORK OUT 5-6 TIMES A WEEK", "DRINK 1 GALLON OF WATER DAILY", 
    "GET 8 HOURS OF SLEEP DAILY", "MAX OUT YOUR PROTEIN DAILY", 
    "READ 10 PAGES DAILY", "COLD SHOWERS DAILY", "10K STEPS DAILY", 
    "WAKE UP BY 5 AM", "NO EXCUSES", "NOTHING BUT 90 DAYS OF PURE DISCIPLINE"
]

days = [str(i) for i in range(1, 32)]

# --- INITIALIZE STATE & AUTO-SEED 16 RULES TO SUPABASE IF EMPTY ---
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
    if user_id:
        try:
            res = supabase.table("habits").select("name").eq("user_id", user_id).execute()
            if res.data:
                loaded_habits = [row["name"] for row in res.data]
            
            # If database has no habits yet, auto-insert all 16 official rules!
            if not loaded_habits:
                for habit in initial_habits:
                    supabase.table("habits").insert({"user_id": user_id, "name": habit}).execute()
                loaded_habits = initial_habits
        except Exception:
            pass
            
    habits_list = loaded_habits if loaded_habits else initial_habits
    grid_data = {day: [False] * len(habits_list) for day in days}
    df = pd.DataFrame(grid_data)
    df.insert(0, "Habit Name", habits_list)
    st.session_state.tracker_df = df

if "sleep_df" not in st.session_state:
    sleep_rows = ["10 hrs", "8 hrs", "6 hrs", "4 hrs", "2 hrs"]
    sleep_data = {day: [False] * len(sleep_rows) for day in days}
    sleep_df = pd.DataFrame(sleep_data)
    sleep_df.insert(0, "Sleep Hours", sleep_rows)
    st.session_state.sleep_df = sleep_df

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
                for i in range(1, 32):
                    new_row[str(i)] = False
                new_df = pd.DataFrame([new_row])
                st.session_state.tracker_df = pd.concat([st.session_state.tracker_df, new_df], ignore_index=True)
                
                # Sync new habit to Supabase
                if user_id:
                    try:
                        supabase.table("habits").insert({"user_id": user_id, "name": new_habit}).execute()
                    except Exception as err:
                        st.error(f"Cloud sync error: {err}")
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

# --- INTERACTIVE LIVE CHART ---
st.subheader("📈 PLAYER MOMENTUM")
daily_totals = st.session_state.tracker_df[days].sum()

fig = px.line(
    x=daily_totals.index, 
    y=daily_totals.values, 
    markers=True,
    labels={"x": "DAY", "y": "QUESTS COMPLETED"}
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
    hovertemplate="Day %{x}<br>Completed: %{y}<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- SLEEP SECTION ---
st.subheader("🌙 FATIGUE RECOVERY")
st.session_state.sleep_df = st.data_editor(
    st.session_state.sleep_df,
    hide_index=True,
    use_container_width=True,
    column_config={"Sleep Hours": st.column_config.Column(disabled=True)}
)
