
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib

# Read the ball-by-ball and matches data from CSV files
balls = pd.read_csv('data/IPL_Ball_by_Ball_2008_2022.csv')
matches = pd.read_csv('data/IPL_Matches_2008_2022.csv')

# Calculate total score for each innings
total_score = balls.groupby(['ID', 'innings']).sum()['total_run'].reset_index()
total_score = total_score[total_score['innings'] == 1]
total_score['target'] = total_score['total_run'] + 1

# Merge matches and total score dataframes based on match ID
match_df = matches.merge(total_score[['ID', 'target']], on='ID')

# Modify team names for consistency
teams = [
    'Rajasthan Royals',
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad',
    'Delhi Capitals',
    'Chennai Super Kings',
    'Gujarat Titans',
    'Lucknow Super Giants',
    'Kolkata Knight Riders',
    'Punjab Kings',
    'Mumbai Indians'
]

match_df['Team1'] = match_df['Team1'].str.replace('Delhi Daredevils', 'Delhi Capitals')
match_df['Team2'] = match_df['Team2'].str.replace('Delhi Daredevils', 'Delhi Capitals')
match_df['WinningTeam'] = match_df['WinningTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')

match_df['Team1'] = match_df['Team1'].str.replace('Kings XI Punjab', 'Punjab Kings')
match_df['Team2'] = match_df['Team2'].str.replace('Kings XI Punjab', 'Punjab Kings')
match_df['WinningTeam'] = match_df['WinningTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')

match_df['Team1'] = match_df['Team1'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
match_df['Team2'] = match_df['Team2'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
match_df['WinningTeam'] = match_df['WinningTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')

# Filter matches dataframe to include only specified teams
match_df = match_df[match_df['Team1'].isin(teams)]
match_df = match_df[match_df['Team2'].isin(teams)]
match_df = match_df[match_df['WinningTeam'].isin(teams)]

# Filter matches with no method and select relevant columns
match_df = match_df[match_df['method'].isna()]
match_df = match_df[['ID', 'City', 'Team1', 'Team2', 'WinningTeam', 'target']].dropna()

# Modify team names in ball-by-ball data for consistency
balls['BattingTeam'] = balls['BattingTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')
balls['BattingTeam'] = balls['BattingTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')
balls['BattingTeam'] = balls['BattingTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')

# Filter ball-by-ball data to include only specified teams
balls = balls[balls['BattingTeam'].isin(teams)]

# Merge match and ball-by-ball dataframes based on match ID
balls_df = match_df.merge(balls, on='ID')

# Filter for the second innings
balls_df = balls_df[balls_df['innings'] == 2]

# Calculate current score, runs left, balls left, wickets left, current run rate, and required run rate
balls_df['current_score'] = balls_df.groupby('ID')['total_run'].cumsum()
balls_df['runs_left'] = np.where(balls_df['target'] - balls_df['current_score'] >= 0, balls_df['target'] - balls_df['current_score'], 0)
balls_df['balls_left'] = np.where(120 - balls_df['overs'] * 6 - balls_df['ballnumber'] >= 0, 120 - balls_df['overs'] * 6 - balls_df['ballnumber'], 0)
balls_df['wickets_left'] = 10 - balls_df.groupby('ID')['isWicketDelivery'].cumsum()
balls_df['current_run_rate'] = (balls_df['current_score'] * 6) / (120 - balls_df['balls_left'])
balls_df['required_run_rate'] = np.where(balls_df['balls_left'] > 0, balls_df['runs_left'] * 6 / balls_df['balls_left'], 0)

# Define a function to determine the match result
def result(row):
    return 1 if row['BattingTeam'] == row['WinningTeam'] else 0

# Apply the result function to determine the match result
balls_df['result'] = balls_df.apply(result, axis=1)

# Update the BowlingTeam based on BattingTeam and Team1/Team2
index1 = balls_df[balls_df['Team2'] == balls_df['BattingTeam']]['Team1'].index
index2 = balls_df[balls_df['Team1'] == balls_df['BattingTeam']]['Team2'].index

balls_df.loc[index1, 'BowlingTeam'] = balls_df.loc[index1, 'Team1']
balls_df.loc[index2, 'BowlingTeam'] = balls_df.loc[index2, 'Team2']

# Select the final columns for the dataframe
final_df = balls_df[['BattingTeam', 'BowlingTeam', 'City', 'runs_left', 'balls_left', 'wickets_left', 'current_run_rate', 'required_run_rate', 'target', 'result']]

# Specify the categorical columns for one-hot encoding
cat_columns = ['BattingTeam', 'BowlingTeam', 'City']

# Perform one-hot encoding on categorical columns
trf = ColumnTransformer([
    ('trf', OneHotEncoder(sparse_output=False, drop='first'), cat_columns)
], remainder='passthrough')

# Split the data into training and test sets
X = final_df.drop('result', axis=1)
y = final_df['result']

print(X.head())

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, test_size=0.01)

# Create the pipeline with logistic regression
pipe = Pipeline(steps=[
    ('step1', trf),
    ('step2', LogisticRegression(solver='liblinear'))
])

# Fit the pipeline on the training data
pipe.fit(X_train, y_train)

# Predict the labels for the test data
y_pred = pipe.predict(X_test)

# Calculate the accuracy score
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the pipeline (including the logistic regression model) using joblib
joblib.dump(pipe, "pipe.joblib")
# Save the ColumnTransformer using joblib
joblib.dump(trf, "column_transformer.joblib")


# export final_df to csv
final_df.to_csv('final_df.csv', index=False)



