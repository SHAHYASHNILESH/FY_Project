import streamlit as st
import joblib
import numpy as np
from joblib import load
import requests
import pandas as pd
import math
import matplotlib.pyplot as plt
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


def get_weather(city_name, api_key="c30889904ca059fafc2004594b099a4e"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_weather_history(city_name, lat, lon, api_key="03653507e6754e49af8155133240305"):
    url = f"http://api.worldweatheronline.com/premium/v1/weather.ashx?key={api_key}&q={city_name}&fx=no&cc=no&mca=yes&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Main Streamlit app
def main():
    st.title("Solar Power Generation Prediction")
    st.markdown(background_image, unsafe_allow_html=True)

    # Inject CSS style for button
    st.markdown(button_styles, unsafe_allow_html=True)

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
        # state = st.selectbox("Select State", states)
        state = st.text_input("Enter State")
        city_name = st.text_input("Enter your city")
        rooftop = st.text_input("Enter your roof-top area(in Sq.Feet)")
        shadow = st.text_input("Enter % of Shadow Free Open Space Available")

        # Assuming you have already collected the user inputs
        rooftop_area_input = rooftop.strip()  # Remove leading and trailing spaces
        shadow_percentage_input = shadow.strip()  # Remove leading and trailing spaces

        # Check if the input is empty
        if rooftop_area_input and shadow_percentage_input:
            # Convert inputs to float
            rooftop_area = float(rooftop_area_input)
            shadow_percentage = float(shadow_percentage_input)

            # Calculate shadowed area
            shadow_area = (shadow_percentage / 100) * rooftop_area

            # Calculate new rooftop area after subtracting shadowed area
            new_rooftop_area = rooftop_area - shadow_area
            new_rooftop_area_sqft = math.ceil(new_rooftop_area / 17.55)

        # city = st.selectbox("Select City", cities[state])

        # Prediction button
        if st.button("Predict", type="secondary"):

            # Display the new rooftop area
            st.write(
                f"<h3 style='color:white;'>New Rooftop Area after subtracting {shadow_percentage}% shadowed area: {new_rooftop_area_sqft:.2f}</h3>",
                unsafe_allow_html=True,
            )

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

            # city_name = st.text_input("Enter city name:")
            # api_key = st.text_input("Enter your OpenWeatherMap API key:")

            if city_name:
                weather_data = get_weather(city_name)

                if weather_data:
                    # st.write("Weather Data:")
                    # st.write(weather_data)

                    # Extract latitude and longitude
                    if "coord" in weather_data:
                        lat = weather_data["coord"]["lat"]
                        lon = weather_data["coord"]["lon"]
                        # st.write(f"Latitude: {lat}, Longitude: {lon}")

                    else:
                        st.write("Latitude and longitude not found in response.")

                    weather_history = get_weather_history(city_name, lat, lon)

                    if weather_history:
                        st.write("Weather History Data:")
                        # st.write(weather_history)
                    else:
                        st.write(
                            "Failed to fetch weather history data. Please check your input and try again."
                        )

                    # Extracting absMaxTemp for each month
                    Temp_array = [
                        float(month_data["absMaxTemp"])
                        for month_data in weather_history["data"]["ClimateAverages"][0][
                            "month"
                        ]
                    ]
                    st.write(Temp_array)

                    # New array for sunlight hours
                    sunlight_hrs = []
                    # Iterate over the temperature array
                    for t in Temp_array:
                        if t < 30:
                            sunlight_hrs.append(round(9 + 0.5 * (t - 30), 2))
                        else:
                            sunlight_hrs.append(round(10 + (t - 30), 2))

                    # Printing the sunlight hours array
                    st.write(sunlight_hrs)
                    # Load the trained model
                    loaded_model = joblib.load(
                        "C:/FY_Project/linear_regression_model_new.pkl"
                    )

                    # Define new data with temperature and daylight hours
                    new_data = pd.DataFrame(
                        {"Temperature (°C)": Temp_array, "Daylight Hours": sunlight_hrs}
                    )

                    # Predict using the loaded model
                    predictions = loaded_model.predict(new_data)

                    # Multiply each element of the predictions array by 30
                    predictions_per_month = [
                        prediction * 30 for prediction in predictions
                    ]

                    # Display the predictions per month
                    st.write("Predicted Power Generation/month:")
                    st.write(predictions_per_month)

                    # Plotting the graph
                    plt.figure(figsize=(10, 6))
                    plt.plot(predictions_per_month, label="Predictions")
                    plt.xlabel("Month")
                    plt.ylabel("Power Generation")
                    plt.title(f"Predicted Power Generation/month for {city_name}")
                    plt.legend()
                    plt.grid(True)
                    st.pyplot(plt)

                else:
                    st.write(
                        "Failed to fetch weather data. Please check your input and try again."
                    )
            else:
                st.write("Please enter both city name and API key.")

    else:
        st.text("Please Login first")


if __name__ == "__main__":
    main()
