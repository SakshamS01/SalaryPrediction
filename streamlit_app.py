import streamlit as st
import pickle
import pandas as pd

# Load the trained model
try:
    with open('random_forest_model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("Model file 'random_forest_model.pkl' not found. Please ensure it's in the same directory.")
    st.stop()

# Title of the app
st.title('Salary Prediction App')
st.write('Enter the employee details to predict their salary.')

# Input fields for features
age = st.slider('Age', 18, 65, 30)
years_of_experience = st.slider('Years of Experience', 0, 40, 5)

gender_options = {'Male': 1, 'Female': 0}
gender_selection = st.selectbox('Gender', list(gender_options.keys()))
gender = gender_options[gender_selection]

education_options = {
    "Bachelor's": 0,
    "Master's": 1,
    "PhD": 2
}
education_level_selection = st.selectbox('Education Level', list(education_options.keys()))
education_level = education_options[education_level_selection]

# For 'Job Title', let's provide a few common examples and allow for manual input
# In a real application, you'd save/load the LabelEncoder for all categories
job_title_options = {
    'Software Engineer': 159,
    'Data Analyst': 17,
    'Senior Manager': 130,
    'Sales Associate': 101,
    'Director': 22,
    'Other (Enter encoded value)': -1 # Placeholder for manual input
}
job_title_selection = st.selectbox('Job Title', list(job_title_options.keys()))

if job_title_selection == 'Other (Enter encoded value)':
    job_title = st.number_input('Enter Encoded Job Title (e.g., 159 for Software Engineer)', min_value=0, max_value=200, value=0)
el_se:
    job_title = job_title_options[job_title_selection]

# Create a DataFrame for prediction
input_data = pd.DataFrame([{
    'Age': age,
    'Gender': gender,
    'Education Level': education_level,
    'Job Title': job_title,
    'Years of Experience': years_of_experience
}])

# Predict button
if st.button('Predict Salary'):
    if job_title == -1: # Check if 'Other' was selected but no value entered
        st.warning('Please enter an encoded value for Job Title if "Other" is selected.')
    else:
        prediction = model.predict(input_data)[0]
        st.success(f'The predicted salary is: ${prediction:,.2f}')
