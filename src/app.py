from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

teams = [
    "Rajasthan Royals",
    "Royal Challengers Bangalore",
    "Sunrisers Hyderabad",
    "Delhi Capitals",
    "Chennai Super Kings",
    "Gujarat Titans",
    "Lucknow Super Giants",
    "Kolkata Knight Riders",
    "Punjab Kings",
    "Mumbai Indians",
]

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_DIR = BASE_DIR / "assets" / "logos"

logos = {
    "Mumbai Indians": str(LOGO_DIR / "MI.png"),
    "Rajasthan Royals": str(LOGO_DIR / "RR.png"),
    "Royal Challengers Bangalore": str(LOGO_DIR / "RCB.png"),
    "Sunrisers Hyderabad": str(LOGO_DIR / "SRH.png"),
    "Delhi Capitals": str(LOGO_DIR / "DC.png"),
    "Chennai Super Kings": str(LOGO_DIR / "CSK.png"),
    "Gujarat Titans": str(LOGO_DIR / "GT.png"),
    "Lucknow Super Giants": str(LOGO_DIR / "LSG.png"),
    "Kolkata Knight Riders": str(LOGO_DIR / "KKR.png"),
    "Punjab Kings": str(LOGO_DIR / "PBKS.png"),
}


def set_bg_hack_url():
    st.markdown(
        f"""
        <style>
         .stApp {{
             background: linear-gradient(to right, #000428, #004e92); /* Dark blue gradient */
             color: white; /* Default text color */
             padding: 1rem;
             font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; /* Modern system font stack */
         }}
         h1 {{ /* For st.title */
             color: #FFD700; /* Gold color */
             text-shadow: 2px 2px 4px #000000; /* Text shadow for depth */
             text-align: center; /* Center title */
             margin-bottom: 1.5rem; /* Add some space below title */
         }}
         /* Styling for labels of selectbox and slider */
         .stSelectbox label, .stSlider label {{
             color: #E0E0E0; /* Lighter color for labels */
             font-size: 1.1em;
             font-weight: bold; /* Make labels a bit more prominent */
         }}
         /* Styling for the button */
         .stButton>button {{
             background-color: #FFD700; /* Gold background */
             color: #000428; /* Dark blue text */
             border-radius: 25px; /* More rounded corners */
             padding: 12px 24px; /* More padding */
             font-size: 1.1em;
             font-weight: bold;
             border: none;
             box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Softer shadow */
             transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease; /* Smooth transitions */
             cursor: pointer; /* Pointer cursor on hover */
         }}
         .stButton>button:hover {{
             background-color: #FFC700; /* Lighter gold on hover */
             transform: translateY(-2px); /* Slight lift on hover */
             box-shadow: 0 6px 12px rgba(0,0,0,0.3); /* Enhanced shadow on hover */
         }}
         .stButton>button:active {{
             transform: translateY(0px); /* Button press effect */
             box-shadow: 0 2px 4px rgba(0,0,0,0.2); /* Smaller shadow on press */
         }}
         /* Styling for images */
         .stImage img {{
            border-radius: 15px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25); /* Enhanced shadow */
         }}
         /* Styling for subheaders (st.subheader) */
         /* Streamlit often renders st.subheader as h2. Targeting both for robustness. */
         h2, .stsubheader {{
            color: #B0C4DE !important; /* Light steel blue. Use !important if strictly needed. */
            text-align: center; /* Center subheaders */
            margin-top: 1.5rem; /* Space above subheader */
            margin-bottom: 1rem; /* Space below subheader */
         }}
         </style>
         """,
        unsafe_allow_html=True,
    )


set_bg_hack_url()

cities = [
    "Ahmedabad",
    "Kolkata",
    "Mumbai",
    "Navi Mumbai",
    "Pune",
    "Dubai",
    "Sharjah",
    "Abu Dhabi",
    "Delhi",
    "Chennai",
    "Hyderabad",
    "Visakhapatnam",
    "Chandigarh",
    "Bengaluru",
    "Jaipur",
    "Indore",
    "Bangalore",
    "Raipur",
    "Ranchi",
    "Cuttack",
    "Dharamsala",
    "Nagpur",
    "Johannesburg",
    "Centurion",
    "Durban",
    "Bloemfontein",
    "Port Elizabeth",
    "Kimberley",
    "East London",
    "Cape Town",
]

pipe = joblib.load(BASE_DIR / "models" / "pipe.joblib")


st.title("IPL Winner Predictor")

default_batting_team = "Mumbai Indians"
default_bowling_team = "Chennai Super Kings"
default_city = "Mumbai"
default_target_score = 180
default_current_score = 100  # Change this to your desired default current score
default_overs_completed = 10  # Change this to your desired default overs completed
default_wickets = 3  # Change this to your desired default wickets

# Default values for new over inputs
default_overs_float = float(default_overs_completed)  # default_overs_completed is int
default_completed_overs_val = int(default_overs_float)
default_balls_val = int(round((default_overs_float - default_completed_overs_val) * 10))

# ... (rest of your code)

col1, col2 = st.columns(2)

# Team selection
with col1:
    batting_team = st.selectbox(
        "Batting Team", teams, index=teams.index(default_batting_team), key="batting"
    )

with col2:
    bowling_team = st.selectbox(
        "Bowling Team", teams, index=teams.index(default_bowling_team), key="bowling"
    )

col3, col4 = st.columns(2)
with col3:
    city = st.selectbox("Host City", cities, index=cities.index(default_city))

with col4:
    target_score = st.number_input(
        "Target Score", min_value=0, max_value=400, value=default_target_score, step=1
    )

# Inputs for current score, overs, and wickets using st.number_input
col5, col6, col7, col8 = st.columns(4)  # Changed to 4 columns

with col5:
    current_score = st.number_input(
        "Current Score", min_value=0, max_value=400, value=default_current_score, step=1
    )

with col6:
    completed_overs = st.number_input(  # New input for completed overs
        "Completed Overs",
        min_value=0,
        max_value=20,
        value=default_completed_overs_val,
        step=1,
        help="Enter the number of fully completed overs (0-20).",
    )

with col7:
    balls_this_over = st.number_input(  # New input for balls in current over
        "Balls (Current Over)",
        min_value=0,
        max_value=5,
        value=default_balls_val,
        step=1,
        help="Enter the number of balls bowled in the current over (0-5).",
    )

with col8:  # Wickets input moved to col8
    wickets = st.number_input(
        "Wickets Out", min_value=0, max_value=10, value=default_wickets, step=1
    )

if st.button("Predict Probability"):
    runs_left = target_score - current_score

    # Calculate total balls bowled from completed_overs and balls_this_over
    # Ensure that if 20 overs are completed, balls_this_over is treated as 0 for calculation if it somehow exceeds that.
    if completed_overs == 20:
        total_balls_bowled = 120
    else:
        total_balls_bowled = min(completed_overs * 6 + balls_this_over, 120)

    balls_left = 120 - total_balls_bowled
    wickets_left = 10 - wickets  # This remains the same

    # Calculate current_run_rate
    if total_balls_bowled > 0:
        # CRR = total runs / (total balls bowled / 6)
        current_run_rate = (current_score * 6.0) / total_balls_bowled
    else:
        current_run_rate = 0.0

    # Calculate required_run_rate
    if balls_left > 0:
        # RRR = runs needed / (balls left / 6)
        required_run_rate = (runs_left * 6.0) / balls_left
    else:  # No balls left
        if runs_left <= 0:  # Target achieved or scores are level
            required_run_rate = 0.0
        else:  # Target not achieved, and runs are still needed
            required_run_rate = (
                999.0  # Representing a very high, practically impossible RRR
            )

    input_df = pd.DataFrame(
        {
            "BattingTeam": [batting_team],
            "BowlingTeam": [bowling_team],
            "City": [city],
            "runs_left": [runs_left],
            "balls_left": [balls_left],
            "wickets_left": [wickets_left],
            "current_run_rate": [current_run_rate],
            "required_run_rate": [required_run_rate],
            "target": [target_score],
        }
    )

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    col6, col7 = st.columns(2)
    with col6:
        st.image(
            logos[batting_team],
            caption=None,
            width=250,
            clamp=False,
            channels="RGB",
            output_format="auto",
        )
        st.subheader(batting_team + ": " + str(round(win * 100)) + "%")
    with col7:
        st.image(
            logos[bowling_team],
            caption=None,
            width=250,
            clamp=False,
            channels="RGB",
            output_format="auto",
        )
        st.subheader(bowling_team + ": " + str(round(loss * 100)) + "%")
    pass
