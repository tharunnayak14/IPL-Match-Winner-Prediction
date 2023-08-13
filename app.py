import streamlit as st
import joblib
import pandas as pd

teams = ['Rajasthan Royals ',
         'Royal Challengers Bangalore',
         'Sunrisers Hyderabad',
         'Delhi Capitals',
         'Chennai Super Kings',
         'Gujarat Titans',
         'Lucknow Super Giants',
         'Kolkata Knight Riders',
         'Punjab Kings',
         'Mumbai Indians']

logos = {'Mumbai Indians': "MI.png",
         'Rajasthan Royals': "RR.png",
         'Royal Challengers Bangalore': "RCB.png",
         'Sunrisers Hyderabad': "SRH.png",
         'Delhi Capitals': "DC.png",
         'Chennai Super Kings': "CSK.png",
         'Gujarat Titans': "GT.png",
         'Lucknow Super Giants': "LSG.png",
         'Kolkata Knight Riders': "KKR.png",
         'Punjab Kings': "PBKS.png",
         }


def set_bg_hack_url():
    st.markdown(
        f"""
        <style>
         .stApp {{
             color: white;
             text-align:center;
             padding: 1rem;
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

set_bg_hack_url()

cities = ['Ahmedabad', 'Kolkata', 'Mumbai', 'Navi Mumbai', 'Pune', 'Dubai',
          'Sharjah', 'Abu Dhabi', 'Delhi', 'Chennai', 'Hyderabad',
          'Visakhapatnam', 'Chandigarh', 'Bengaluru', 'Jaipur', 'Indore',
          'Bangalore', 'Raipur', 'Ranchi', 'Cuttack', 'Dharamsala', 'Nagpur',
          'Johannesburg', 'Centurion', 'Durban', 'Bloemfontein',
          'Port Elizabeth', 'Kimberley', 'East London', 'Cape Town']

pipe = joblib.load('pipe.joblib')


st.title("IPL Winner Predictor")

default_batting_team = 'Mumbai Indians'
default_bowling_team = 'Chennai Super Kings'
default_city = 'Mumbai'
default_target_score = 180
default_current_score = 100  # Change this to your desired default current score
default_overs_completed = 10  # Change this to your desired default overs completed
default_wickets = 3  # Change this to your desired default wickets

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
    target_score = st.slider("Target Score", 0, 300, default_target_score)

# Sliders for current score, overs, and wickets
col5, col6, col7 = st.columns(3)

with col5:
    current_score = st.slider("Current Score", 0, 300, default_current_score)

with col6:
    overs_completed = st.slider("Overs Completed", 0, 20, default_overs_completed)

with col7:
    wickets = st.slider("Wickets Out", 0, 10, default_wickets)

if st.button("Predict Probability"):
    runs_left = target_score - current_score
    balls_left = 120 - (overs_completed*6)
    wickets_left = 10 - wickets
    current_run_rate = current_score/overs_completed
    required_run_rate = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'BattingTeam': [batting_team],
                             'BowlingTeam': [bowling_team],
                             'City': [city],
                             'runs_left': [runs_left],
                             'balls_left': [balls_left],
                             'wickets_left': [wickets_left],
                             'current_run_rate': [current_run_rate],
                             'required_run_rate': [required_run_rate],
                             'target': [target_score]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    col6, col7 = st.columns(2)
    with col6:
        st.image(logos[batting_team], caption=None, width=250,
                 clamp=False, channels="RGB", output_format="auto")
        st.subheader(batting_team + ': ' + str(round(win * 100)) + '%')
    with col7:
        st.image(logos[bowling_team], caption=None, width=250,
                 clamp=False, channels="RGB", output_format="auto")
        st.subheader(bowling_team + ': ' + str(round(loss * 100)) + '%')
    pass

