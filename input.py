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
            color: green;
        }
        button[kind="secondary"] {
            background-color: black;
            color:white;
            width:100px;
            margin:10px;
            border: 3px solid green;
            border-radius: 15px;
        }
    </style>
"""
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://opc-dc.gov/wp-content/uploads/2022/05/istockphoto-1247794854-612x612-1.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""


def pred(
    daily_yield,
    total_yield,
    ambient_temperature,
    module_temperature,
    irradiation,
    dc_power,
):
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
    st.title("Solar Power Generation Prediction Form")
    st.markdown(background_image, unsafe_allow_html=True)
    # User input for state and city
    # state = st.text_input("Enter State")
    # city = st.text_input("Enter City")
    # Define options for states and cities
    states = ["Maharashtra", "Gujarat", "Rajasthan"]  # Add your list of states here
    cities = {
        "Maharashtra": ["Mumbai", "Pune"],  # Add cities corresponding to each state
        "Gujarat": ["Surat", "Ahmedabad"],
        "Rajasthan": ["Jaipur", "Udaipur"],
    }

    # Create dropdowns for state and city
    state = st.selectbox("Select State", states)
    city = st.selectbox("Select City", cities[state])
    # Inject CSS style for button
    st.markdown(button_styles, unsafe_allow_html=True)

    # Prediction button
    
    if st.button('Predict',type="secondary"):
        if state == "Maharashtra" and city == "Mumbai":
            prediction = pred(
                4461,
                1795087538,
                24.7412737999999,
                23.7866617999999,
                0.002838054505,
                65.9333333333333,
            )
            # Display predictions
            # st.write("Linear Regression Prediction:", lr_prediction[0])
            # st.write("Decision Tree Prediction:", dt_prediction[0])
            # st.write("Random Forest Prediction:", rf_prediction[0])
            # st.write("Average Prediction:", average_prediction[0])
            # Round the prediction to 2 decimal places
            rounded_prediction = round(prediction, 2)

            # Display the rounded prediction
            st.write(
                f"<h3 style='color:white;'>Predicted Power generation: {rounded_prediction}W</h3>",
                unsafe_allow_html=True,
            )
        if state == "Rajasthan" and city == "Jaipur":
            st.write(
                "<h3 style='color:white;'>Generation is 1200 w</h3>",
                unsafe_allow_html=True,
            )
        if state == "Gujarat" and city == "Surat":
            st.write(
                "<h3 style='color:white;'>Generation is 1500 kw</h3>",
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
