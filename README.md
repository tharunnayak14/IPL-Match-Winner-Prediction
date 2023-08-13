# IPL Winner Predictor

![IPL Winner Predictor](project_screenshot.png)

IPL Winner Predictor is a web application built using Streamlit that predicts the probability of a cricket team winning an IPL match based on various input parameters such as batting team, bowling team, host city, current score, overs completed, wickets, and more.

## Features

- User-friendly interface with interactive sliders and dropdowns.
- Displays team logos and predicted win/loss probabilities.
- Provides insights into the match outcome based on real-time data.

## How to Use

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the Streamlit app using `streamlit run app.py`.
4. Fill in the required inputs:
   - Select the batting and bowling teams from the dropdowns.
   - Choose the host city, target score, current score, overs completed, and wickets.
5. Click the "Predict Probability" button to see the predicted win/loss probabilities.

## Tech Stack

- Python
- Streamlit
- Joblib
- Pandas

## Project Structure

- `app.py`: Main Streamlit application script.
- `pipe.joblib`: Pre-trained machine learning pipeline for prediction.
- `teams_logos/`: Folder containing team logos.
- `requirements.txt`: List of required Python packages.

## Screenshots

![Team Selection](screenshots/team_selection.png)
![Predicted Results](screenshots/predicted_results.png)

## Author

- Your Name
- GitHub: [Your GitHub Profile](https://github.com/yourusername)

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to fork, contribute, and make this project even better!
