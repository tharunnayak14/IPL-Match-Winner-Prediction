import streamlit as st
import pickle
import pandas as pd

teams = ['Rajasthan Royals',
     'Royal Challengers Bangalore',
     'Sunrisers Hyderabad',
     'Delhi Capitals',
     'Chennai Super Kings',
     'Gujarat Titans',
     'Lucknow Super Giants',
     'Kolkata Knight Riders',
     'Punjab Kings',
     'Mumbai Indians']


def set_bg_hack_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://wallpaperaccess.com/full/2302746.jpg");
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )
# set_bg_hack_url()
cities = ['Ahmedabad', 'Kolkata', 'Mumbai', 'Navi Mumbai', 'Pune', 'Dubai',
       'Sharjah', 'Abu Dhabi', 'Delhi', 'Chennai', 'Hyderabad',
       'Visakhapatnam', 'Chandigarh', 'Bengaluru', 'Jaipur', 'Indore',
       'Bangalore', 'Raipur', 'Ranchi', 'Cuttack', 'Dharamsala', 'Nagpur',
       'Johannesburg', 'Centurion', 'Durban', 'Bloemfontein',
       'Port Elizabeth', 'Kimberley', 'East London', 'Cape Town']

pipe = pickle.load(open('pipe.pkl','rb'))

st.title("IPL Predictor")

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Select the batting team", sorted(teams))
with col2:
    bowling_team = st.selectbox("Select the bowling team", sorted(teams))

city = st.selectbox("Select the host city", sorted(cities))
target_score = st.number_input("Enter the target score")

col3, col4, col5 = st.columns(3)

with col3:
    current_score = st.number_input("Enter current score")
with col4:
    overs_completed = st.number_input("Enter overs completed")
with col5:
    wickets = st.number_input("Wickets out")

if st.button("Predict Probability"):
    runs_left = target_score - current_score
    balls_left = 120 - (overs_completed*6)
    wickets_left = 10 - wickets
    current_run_rate = current_score/overs_completed
    required_run_rate = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'BattingTeam':[batting_team],
                  'BowlingTeam':[bowling_team],
                  'City':[city],
                  'runs_left':[runs_left],
                  'balls_left':[balls_left],
                  'wickets_left':[wickets_left],
                  'current_run_rate':[current_run_rate],
                  'required_run_rate':[required_run_rate],
                  'target':[target_score]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + '- '+ str(round(win*100)) + '%')
    st.header(bowling_team + '- '+ str(round(loss*100))+ '%')
    # st.header(str(result))

    pass
