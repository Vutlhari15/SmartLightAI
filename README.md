# SmartLight AI: AI-Powered Streetlight Fault Detection

## Project Overview
SmartLight AI is a machine learning prototype that classifies streetlight operating conditions and identifies potential faults using electrical and environmental data.

## Objectives
- Identify potential streetlight faults using machine learning.
- Classify streetlight records into fault categories.
- Present predictions through a dashboard.
- Support more efficient streetlight maintenance planning.

## Fault Categories
- No Fault
- Short Circuit
- Voltage Surge
- Bulb Failure
- Light Flickering

## Technologies Used
- Python
- Pandas
- Scikit-learn
- Streamlit
- CSV datasets
- Git and GitHub

## Machine Learning Approach
The project uses a Random Forest classifier trained on labelled streetlight data. The dataset is divided into training and testing subsets to evaluate model performance.

## Dataset
The project uses the Street Light Fault Prediction Dataset from Kaggle:

https://www.kaggle.com/datasets/vizeno/street-light-fault-prediction-dataset

## How to Run
1. Install Python.
2. Install the required packages:
   `pip install streamlit pandas scikit-learn`
3. Run the dashboard:
   `streamlit run app.py`

Additional dependencies may be required depending on the project environment.

## Limitations
This is a prototype that uses a dataset rather than live streetlight sensors. Predictions require further testing with real-world data before use in municipal operations.

## Future Improvements
- Test with real streetlight sensor data.
- Improve fault classification performance.
- Explore integration with municipal maintenance systems.
