import streamlit as st
import joblib
import numpy as np
from joblib import load
from firebase_admin import credentials, firestore, initialize_app, storage

# if not firebase_admin._apps:
#     # Initialize Firebase
#     cred = credentials.Certificate("fy-project-a9188-c7e54655ad87.json")
#     # print(cred)
#     firebase_admin.initialize_app(cred)

# db = firestore.client()


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
    st.title("Solar Power Generation Prediction")
    st.markdown(background_image, unsafe_allow_html=True)
    # User input for state and city
    # state = st.text_input("Enter State")
    # city = st.text_input("Enter City")
    # Define options for states and cities
    if st.session_state.username != "":
        states = [
            "Andhra Pradesh",
            "Arunachal Pradesh",
            "Assam",
            "Bihar",
            "Chhattisgarh",
            "Goa",
            "Gujarat",
            "Haryana",
            "Himachal Pradesh",
            "Jammu and Kashmir",
            "Jharkhand",
            "Karnataka",
            "Kerala",
            "Madhya Pradesh",
            "Maharashtra",
            "Manipur",
            "Meghalaya",
            "Mizoram",
            "Nagaland",
            "Odisha",
            "Punjab",
            "Rajasthan",
            "Sikkim",
            "Tamil Nadu",
            "Telangana",
            "Tripura",
            "Uttarakhand",
            "Uttar Pradesh",
            "West Bengal",
            "Andaman and Nicobar Islands",
            "Chandigarh",
            "Dadra and Nagar Haveli",
            "Daman and Diu",
            "Delhi",
            "Lakshadweep",
            "Puducherry",
        ]
        # cities = {
        #     "Maharashtra": ["Mumbai", "Pune"],  # Add cities corresponding to each state
        #     "Gujarat": ["Surat", "Ahmedabad"],
        #     "Rajasthan": ["Jaipur", "Udaipur"],
        # }

        # Create dropdowns for state and city
        state = st.selectbox("Select State", states)
        # city = st.selectbox("Select City", cities[state])
        # Inject CSS style for button
        st.markdown(button_styles, unsafe_allow_html=True)

        # Prediction button

        if st.button("Predict", type="secondary"):
            if state == "Maharashtra" or state == "Goa":
                # prediction = pred(
                #     4461,
                #     1795087538,
                #     24.7412737999999,
                #     23.7866617999999,
                #     0.002838054505,
                #     65.9333333333333,
                # )
                # Display predictions
                # st.write("Linear Regression Prediction:", lr_prediction[0])
                # st.write("Decision Tree Prediction:", dt_prediction[0])
                # st.write("Random Forest Prediction:", rf_prediction[0])
                # st.write("Average Prediction:", average_prediction[0])
                # Round the prediction to 2 decimal places
                # rounded_prediction = round(prediction, 2)

                # Display the rounded prediction
                # st.write(
                #     f"<h3 style='color:white;'>Predicted Power generation: {rounded_prediction}W</h3>",
                #     unsafe_allow_html=True,
                # )
                st.write(
                    f"<h3 style='color:white;'>Predicted Power generation/month:120 units(1 kg)</h3>",
                    unsafe_allow_html=True,
                )
            elif state == "Rajasthan":
                st.write(
                    "<h3 style='color:white;'>Predicted Power generation/month:127 units(1 kg)</h3>",
                    unsafe_allow_html=True,
                )
            elif state == "Gujarat":
                st.write(
                    "<h3 style='color:white;'>Predicted Power generation/month:127 units(1 kg)</h3>",
                    unsafe_allow_html=True,
                )
            elif state == "Delhi":
                st.write(
                    "<h3 style='color:white;'>Predicted Power generation/month:115 units(1 kg)</h3>",
                    unsafe_allow_html=True,
                )
            elif state == "Jammu and Kashmir":
                st.write(
                    "<h3 style='color:white;'>Predicted Power generation/month:95 units(1 kg)</h3>",
                    unsafe_allow_html=True,
                )
            elif (
                state == "Himachal Pradesh"
                or state == "Punjab"
                or state == "Chandigarh"
                or state == "Uttarakhand"
            ):
                st.write(
                    "<h3 style='color:white;'>Predicted Power generation/month:110 units(1 kg)</h3>",
                    unsafe_allow_html=True,
                )
            elif (
                state == "Andhra Pradesh"
                or state == "Karnataka"
                or state == "Kerala"
                or state == "Tamil Nadu"
            ):
                st.write(
                    "<h3 style='color:white;'>Predicted Power generation/month:127 units(1 kg)</h3>",
                    unsafe_allow_html=True,
                )
            elif (
                state == "Uttar Pradesh"
                or state == "Bihar"
                or state == "Jharkhand"
                or state == "Madhya Pradesh"
            ):
                st.write(
                    "<h3 style='color:white;'>Predicted Power generation/month:122 units(1 kg)</h3>",
                    unsafe_allow_html=True,
                )
            else:
                st.write(
                    "<h3 style='color:white;'>Predicted Power generation/month:120 units(1 kg)</h3>",
                    unsafe_allow_html=True,
                )

            st.write(
                "<h3 style='color:white;'>There are 2 major varieties available:</h3>",
                unsafe_allow_html=True,
            )
            st.write(
                "<h5 style='color:white;'>Rs. 18,000 is for solar panels which generate 550 Watt of electricity and weight is around 28kg.</h5>",
                unsafe_allow_html=True,
            )
            st.write(
                "<h5 style='color:white;'>Rs. 11,500 is for solar panels which generate 350 Watt of electricity and weight is around 28kg.</h5>",
                unsafe_allow_html=True,
            )
            st.write(
                "<h5 style='color:white;font-size:27px;'>For further inquiry, Contact: <a href='tel:+919422161101'>+91 94221 61101</a></h5>",
                unsafe_allow_html=True,
            )

    else:
        st.text("Please Login first")


if __name__ == "__main__":
    main()
