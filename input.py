import streamlit as st
import joblib
import numpy as np
from joblib import load

# from joblib.compat import pickle

# CSS style for prediction button
button_styles = """
    <style>
        .orange-button {
            background-color: green;
            color: white;
            border: 2px solid green;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 18px;
            cursor: pointer;
            transition: background-color 0.3s, color 0.3s;
        }
        .orange-button:hover {
            background-color: white;
            color: orange;
        }
    </style>
"""
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("data:image/jpeg;base64,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");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

def pred(daily_yield,total_yield,ambient_temperature,module_temperature,irradiation,dc_power):
    # Load the models
    lr_model = joblib.load("C:/FY_Project/linear_regression_model.pkl")
    dt_model = joblib.load("C:/FY_Project/decision_tree_model.pkl")
    rf_model = joblib.load("C:/FY_Project/random_forest_model.pkl")

    # # Sidebar with user input
    # st.sidebar.title("Input Parameters")
    # irradiation = st.sidebar.number_input("IRRADIATION", value=0.002838054505)
    # daily_yield = st.sidebar.number_input("DAILY YIELD", value=4461)
    # module_temperature = st.sidebar.number_input(
    #         "MODULE TEMPERATURE", value=23.7866617999999
    # )
    # ambient_temperature = st.sidebar.number_input(
    #         "AMBIENT TEMPERATURE", value=24.7412737999999
    # )
    # total_yield = st.sidebar.number_input("TOTAL YIELD", value=1795087538)
    # dc_power = st.sidebar.number_input("DC POWER", value=65.9333333333333)

    # Create testing data
    testing_new = np.array(
            [
                daily_yield,
                total_yield,
                ambient_temperature,
                module_temperature,
                irradiation,
                dc_power,
            ]
    ).reshape(1, -1)

    # Make predictions using each model
    lr_prediction = lr_model.predict(testing_new)
    dt_prediction = dt_model.predict(testing_new)
    rf_prediction = rf_model.predict(testing_new)
    average_prediction = (lr_prediction + dt_prediction + rf_prediction) / 3

    return average_prediction[0]


# Main Streamlit app
def main():
    st.title("Prediction Form")
    st.markdown(background_image, unsafe_allow_html=True)
    # User input for state and city
    state = st.text_input("Enter State")
    city = st.text_input("Enter City")

    # Inject CSS style for button
    st.markdown(button_styles, unsafe_allow_html=True)

    # Prediction button
    if st.button("Predict"):
        if state and city:
            # Perform prediction based on input
            st.write(
                f"<h3 style='color:white;'>Prediction for {state} , {city}</h3>",
                unsafe_allow_html=True,
            )
        else:
            st.error("Please enter both State and City.")
    if state == "Maharashtra" and city == "Mumbai":
       prediction=pred(4461,1795087538,24.7412737999999,23.7866617999999,0.002838054505,65.9333333333333)
       # Display predictions
        # st.write("Linear Regression Prediction:", lr_prediction[0])
        # st.write("Decision Tree Prediction:", dt_prediction[0])
        # st.write("Random Forest Prediction:", rf_prediction[0])
        # st.write("Average Prediction:", average_prediction[0])
       st.write(
                f"<h3 style='color:white;'>Predicted Power generation:{prediction}</h3>",
                unsafe_allow_html=True,
       )
       if state == "Rajasthan" and city == "Jaipur":
            st.write(
                "<h3 style='color:white;'>Generation is 1200 kw</h3>",
                unsafe_allow_html=True,
            )
       if state == "Gujrat" and city == "Surat":
            st.write(
                "<h3 style='color:white;'>Generation is 1500 kw</h3>",
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
