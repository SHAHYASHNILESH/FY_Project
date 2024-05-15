import streamlit as st
import joblib
import numpy as np
from joblib import load
import requests
import pandas as pd
import math
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import time
import plotly.express as px

matplotlib.use("TkAgg")  # Set the backend to TkAgg
import mplcursors
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
        button[kind="secondary"] {
            background-color: black;
            color:white;
            width:7%;
            margin:10px;
            border: 2px solid white;
            border-radius: 15px;
        }

        .css-1y4p8pa{
            max-width:none;
            padding-left:7rem;
            padding-top:0px;
        }

        .css-k7vsyb span{
            color: #FFFFFF;
            font-size: 40px;
        }

        .css-16idsys p {
            word-break: break-word;
            margin-bottom: -1px;
            font-size: 35px;
            color: black;
            font-weight: bolder;
        }
        .css-1vbkxwb p {
            word-break: break-word;
            margin-bottom: 0px;
            font-size: 20px;

        }
        .css-10trblm {
            position: relative;
            flex: 1 1 0%;
            margin-left: calc(3rem);
            color: black;
            font-weight: bolder;
            font-size: 30px;
        }
        .st-dn{
            font-size:150%;
        }
        .st-cd{
            font-size:150%;
        }
        img{
            width:150% !important;
            align-items:center;
        }
        [data-testid="stAppViewContainer"] > .main{
            background-image: url(data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxISEhUSEhIVFRUVFxcVFxcXFxcaFxcVFRcXFxUXFRcYHSggGBolHRUXITEiJSkrLi4uFx8zODMtNygtLisBCgoKDQ0NDg0NDisZFRk3LSsrNysrKystKy0rKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrK//AABEIALcBEwMBIgACEQEDEQH/xAAYAAEBAQEBAAAAAAAAAAAAAAACAQADB//EAB4QAQEBAQEAAgMBAAAAAAAAAAABEQISgfBRcZEx/8QAFgEBAQEAAAAAAAAAAAAAAAAAAAEC/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8A8oirFVlIrSFgJFxcWQExYuKCYshYuAmNIUi4A4vlauAmNiz/AFcAcXFkXAHGwkAbEw8TACxsPEBzxrDxMAKNPEoOeMViWAI0sYBSwkAWXGAoyQpAWLEhA2FGiyA0irFgJhSNIsgNIsi4oCuLiyAMWFi+RRxsLGwBawsawAxsPEwAsSw8QQLEsPBsALBp2JYAYNOpQAcMaA1KVggjMoKuKsBoUSHAZY0hYDRcWRZAWRY0iwGxrFYElKMUBFnK+SkFGoWNgDIxWNYAISAKWFiWCDRq1KAjTTACwa6WBQBCqUBsGlUqg6rMgUXEiqFCGQ5EFhRIsAljSLAUh5OA0WxlAcJcXmAkhRJFBlxVooWIeJQCxCqCA1WpQCpYSANiWQrBoDYFOjQCxKVg1QEp0QHGVgJtTkoCylEixA+aXIwpAKLBKAUKDCgKUEgZcZQbFitgqFUiwGqWENEGxFSgKUhAaNKoAotQBGmFAaNLoelBRaNBmT5YFhJCgLF5aKgpRIUAosiQoCw5BhQFVFgFixIUoKuDDgo2LKrUEGlI1EBsKjoDg0hoDaNKwbAQaVAEqUqFBKNIaoNg0qNAWZgKFAhwChQIcqBQoBQChhDgLiz9soLFgrAOLBigcUdWASprCqKpREsFfv38pQTBpYNAaNMKA0aVGgKVbEoDRtKwaoNGlRoIyMCw4EIChQIUqBwoEOAUKDFlA4UDS0C1aOrAUkSAcXQ1dA5W9C2gUa1NS0FtBalBEtaoDC1S0EoqNBKJDVBSrUoDRxUoJ/WZgaLBhQChQYsA10YUQItDSgHKQRYBtEUCiwC5oLF0WgEQ6loHo2po2gWoyaC2ilTQa0dWoCUV1LQSi1qKNRq9BQbRq6lBGZgQhXQOFHOFED1eQhyAcUSlBdXRlWAfJSucq6DpqyufJSgbaHprQPWGVAJrR1qBDqa2g2o2pQYda1NBhtbUtUZEsQGo2tUoMlSNQTWRgZZRiygUpQJSiDpysoRYocLXOUpUDjDKsoEsFQIvQa0oHKwxgPW0dTQNNRtBWHWBqlbR0GStRqi1KkTQa1K2paCI1qUGqVKwN8smsCKzILqxmAtWVmAljMoq6zAsVmQXVlZgW9NazAkrarA2pemYG1tZlBvQyswMjMCaNrMCVKzAmozAw2swJjMwP//Z);
            background-size: 100vw 100vh;
            background-repeat: no-repeat;
        }
    </style>
"""
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://t3.ftcdn.net/jpg/05/54/51/40/360_F_554514065_A5Y17mmaZgxkbcKri1g52RrLDtLzOU54.jpg");
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


def get_weather_history(city_name,api_key="0d4122627da444959fa105007241205"):
    url = f"http://api.worldweatheronline.com/premium/v1/weather.ashx?key={api_key}&q={city_name}&fx=no&cc=no&mca=yes&format=json"
    response = requests.get(url,timeout=10)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Main Streamlit app
def main():
    st.title("Solar Power Generation Prediction")
    # st.markdown(background_image, unsafe_allow_html=True)
    st.markdown(button_styles, unsafe_allow_html=True)

    # Inject CSS style for button
    st.markdown(button_styles, unsafe_allow_html=True)

    # User input for state and city
    # state = st.text_input("Enter State")
    # city = st.text_input("Enter City")

    # Define options for states and cities
    if st.session_state.username != "":

        # state = st.text_input("Enter State")
        # city_name = st.text_input("Enter your city")

        # Define a dictionary mapping states to cities
        state_cities = {
            "Andaman and Nicobar Islands (union territory)": ["Port Blair"],
            "Andhra Pradesh": [
                "Adoni",
                "Amaravati",
                "Anantapur",
                "Chandragiri",
                "Chittoor",
                "Dowlaiswaram",
                "Eluru",
                "Guntur",
                "Kadapa",
                "Kakinada",
                "Kurnool",
                "Machilipatnam",
                "Nagarjunakoṇḍa",
                "Rajahmundry",
                "Srikakulam",
                "Tirupati",
                "Vijayawada",
                "Visakhapatnam",
                "Vizianagaram",
                "Yemmiganur",
            ],
            "Arunachal Pradesh": ["Itanagar"],
            "Assam": [
                "Dhuburi",
                "Dibrugarh",
                "Dispur",
                "Guwahati",
                "Jorhat",
                "Nagaon",
                "Sivasagar",
                "Silchar",
                "Tezpur",
                "Tinsukia",
            ],
            "Bihar": [
                "Ara",
                "Barauni",
                "Begusarai",
                "Bettiah",
                "Bhagalpur",
                "Bihar Sharif",
                "Bodh Gaya",
                "Buxar",
                "Chapra",
                "Darbhanga",
                "Dehri",
                "Dinapur Nizamat",
                "Gaya",
                "Hajipur",
                "Jamalpur",
                "Katihar",
                "Madhubani",
                "Motihari",
                "Munger",
                "Muzaffarpur",
                "Patna",
                "Purnia",
                "Pusa",
                "Saharsa",
                "Samastipur",
                "Sasaram",
                "Sitamarhi",
                "Siwan",
            ],
            "Chandigarh (union territory)": ["Chandigarh"],
            "Chhattisgarh": [
                "Ambikapur",
                "Bhilai",
                "Bilaspur",
                "Dhamtari",
                "Durg",
                "Jagdalpur",
                "Raipur",
                "Rajnandgaon",
            ],
            "Dadra and Nagar Haveli and Daman and Diu (union territory)": [
                "Daman",
                "Diu",
                "Silvassa",
            ],
            "Delhi (national capital territory)": ["Delhi", "New Delhi"],
            "Goa": ["Madgaon", "Panaji"],
            "Gujarat": [
                "Ahmadabad",
                "Amreli",
                "Bharuch",
                "Bhavnagar",
                "Bhuj",
                "Dwarka",
                "Gandhinagar",
                "Godhra",
                "Jamnagar",
                "Junagadh",
                "Kandla",
                "Khambhat",
                "Kheda",
                "Mahesana",
                "Morbi",
                "Nadiad",
                "Navsari",
                "Okha",
                "Palanpur",
                "Patan",
                "Porbandar",
                "Rajkot",
                "Surat",
                "Surendranagar",
                "Valsad",
                "Veraval",
            ],
            "Haryana": [
                "Ambala",
                "Bhiwani",
                "Chandigarh",
                "Faridabad",
                "Firozpur Jhirka",
                "Gurugram",
                "Hansi",
                "Hisar",
                "Jind",
                "Kaithal",
                "Karnal",
                "Kurukshetra",
                "Panipat",
                "Pehowa",
                "Rewari",
                "Rohtak",
                "Sirsa",
                "Sonipat",
            ],
            "Himachal Pradesh": [
                "Bilaspur",
                "Chamba",
                "Dalhousie",
                "Dharmshala",
                "Hamirpur",
                "Kangra",
                "Kullu",
                "Mandi",
                "Nahan",
                "Shimla",
                "Una",
            ],
            "Jammu and Kashmir (union territory)": [
                "Anantnag",
                "Baramula",
                "Doda",
                "Gulmarg",
                "Jammu",
                "Kathua",
                "Punch",
                "Rajouri",
                "Srinagar",
                "Udhampur",
            ],
            "Jharkhand": [
                "Bokaro",
                "Chaibasa",
                "Deoghar",
                "Dhanbad",
                "Dumka",
                "Giridih",
                "Hazaribag",
                "Jamshedpur",
                "Jharia",
                "Rajmahal",
                "Ranchi",
                "Saraikela",
            ],
            "Karnataka": [
                "Badami",
                "Ballari",
                "Bengaluru",
                "Belagavi",
                "Bhadravati",
                "Bidar",
                "Chikkamagaluru",
                "Chitradurga",
                "Davangere",
                "Halebid",
                "Hassan",
                "Hubballi-Dharwad",
                "Kalaburagi",
                "Kolar",
                "Madikeri",
                "Mandya",
                "Mangaluru",
                "Mysuru",
                "Raichur",
                "Shivamogga",
                "Shravanabelagola",
                "Shrirangapattana",
                "Tumakuru",
                "Vijayapura",
            ],
            "Kerala": [
                "Alappuzha",
                "Vatakara",
                "Idukki",
                "Kannur",
                "Kochi",
                "Kollam",
                "Kottayam",
                "Kozhikode",
                "Mattancheri",
                "Palakkad",
                "Thalassery",
                "Thiruvananthapuram",
                "Thrissur",
            ],
            "Ladakh (union territory)": ["Kargil", "Leh"],
            "Madhya Pradesh": [
                "Balaghat",
                "Barwani",
                "Betul",
                "Bharhut",
                "Bhind",
                "Bhojpur",
                "Bhopal",
                "Burhanpur",
                "Chhatarpur",
                "Chhindwara",
                "Damoh",
                "Datia",
                "Dewas",
                "Dhar",
                "Dr. Ambedkar Nagar (Mhow)",
                "Guna",
                "Gwalior",
                "Hoshangabad",
                "Indore",
                "Itarsi",
                "Jabalpur",
                "Jhabua",
                "Khajuraho",
                "Khandwa",
                "Khargone",
                "Maheshwar",
                "Mandla",
                "Mandsaur",
                "Morena",
                "Murwara",
                "Narsimhapur",
                "Narsinghgarh",
                "Narwar",
                "Neemuch",
                "Nowgong",
                "Orchha",
                "Panna",
                "Raisen",
                "Rajgarh",
                "Ratlam",
                "Rewa",
                "Sagar",
                "Sarangpur",
                "Satna",
                "Sehore",
                "Seoni",
                "Shahdol",
                "Shajapur",
                "Sheopur",
                "Shivpuri",
                "Ujjain",
                "Vidisha",
            ],
            "Maharashtra": [
                "Ahmadnagar",
                "Akola",
                "Amravati",
                "Aurangabad",
                "Bhandara",
                "Bhusawal",
                "Bid",
                "Buldhana",
                "Chandrapur",
                "Daulatabad",
                "Dhule",
                "Jalgaon",
                "Kalyan",
                "Karli",
                "Kolhapur",
                "Mahabaleshwar",
                "Malegaon",
                "Matheran",
                "Mumbai",
                "Nagpur",
                "Nanded",
                "Nashik",
                "Osmanabad",
                "Pandharpur",
                "Parbhani",
                "Pune",
                "Ratnagiri",
                "Sangli",
                "Satara",
                "Sevagram",
                "Solapur",
                "Thane",
                "Ulhasnagar",
                "Vasai-Virar",
                "Wardha",
                "Yavatmal",
            ],
            "Manipur": ["Imphal"],
            "Meghalaya": ["Cherrapunji", "Shillong"],
            "Mizoram": ["Aizawl", "Lunglei"],
            "Nagaland": ["Kohima", "Mon", "Phek", "Wokha", "Zunheboto"],
            "Odisha": [
                "Balangir",
                "Baleshwar",
                "Baripada",
                "Bhubaneshwar",
                "Brahmapur",
                "Cuttack",
                "Dhenkanal",
                "Kendujhar",
                "Konark",
                "Koraput",
                "Paradip",
                "Phulabani",
                "Puri",
                "Sambalpur",
                "Udayagiri",
            ],
            "Puducherry (union territory)": ["Karaikal", "Mahe", "Puducherry", "Yanam"],
            "Punjab": [
                "Amritsar",
                "Batala",
                "Chandigarh",
                "Faridkot",
                "Firozpur",
                "Gurdaspur",
                "Hoshiarpur",
                "Jalandhar",
                "Kapurthala",
                "Ludhiana",
                "Nabha",
                "Patiala",
                "Rupnagar",
                "Sangrur",
            ],
            "Rajasthan": [
                "Abu",
                "Ajmer",
                "Alwar",
                "Amer",
                "Barmer",
                "Beawar",
                "Bharatpur",
                "Bhilwara",
                "Bikaner",
                "Bundi",
                "Chittaurgarh",
                "Churu",
                "Dhaulpur",
                "Dungarpur",
                "Ganganagar",
                "Hanumangarh",
                "Jaipur",
                "Jaisalmer",
                "Jalor",
                "Jhalawar",
                "Jhunjhunu",
                "Jodhpur",
                "Kishangarh",
                "Kota",
                "Merta",
                "Nagaur",
                "Nathdwara",
                "Pali",
                "Phalodi",
                "Pushkar",
                "Sawai Madhopur",
                "Shahpura",
                "Sikar",
                "Sirohi",
                "Tonk",
                "Udaipur",
            ],
            "Sikkim": ["Gangtok", "Gyalshing", "Lachung", "Mangan"],
            "Tamil Nadu": [
                "Arcot",
                "Chengalpattu",
                "Chennai",
                "Chidambaram",
                "Coimbatore",
                "Cuddalore",
                "Dharmapuri",
                "Dindigul",
                "Erode",
                "Kanchipuram",
                "Kanniyakumari",
                "Kodaikanal",
                "Kumbakonam",
                "Madurai",
                "Mamallapuram",
                "Nagappattinam",
                "Nagercoil",
                "Palayamkottai",
                "Pudukkottai",
                "Rajapalayam",
                "Ramanathapuram",
                "Salem",
                "Thanjavur",
                "Tiruchchirappalli",
                "Tirunelveli",
                "Tiruppur",
                "Thoothukudi",
                "Udhagamandalam",
                "Vellore",
            ],
            "Telangana": [
                "Hyderabad",
                "Karimnagar",
                "Khammam",
                "Mahbubnagar",
                "Nizamabad",
                "Sangareddi",
                "Warangal",
            ],
            "Tripura": ["Agartala"],
            "Uttar Pradesh": [
                "Agra",
                "Aligarh",
                "Amroha",
                "Ayodhya",
                "Azamgarh",
                "Bahraich",
                "Ballia",
                "Banda",
                "Bara Banki",
                "Bareilly",
                "Basti",
                "Bijnor",
                "Bithur",
                "Budaun",
                "Bulandshahr",
                "Deoria",
                "Etah",
                "Etawah",
                "Faizabad",
                "Farrukhabad-cum-Fatehgarh",
                "Fatehpur",
                "Fatehpur Sikri",
                "Ghaziabad",
                "Ghazipur",
                "Gonda",
                "Gorakhpur",
                "Hamirpur",
                "Hardoi",
                "Hathras",
                "Jalaun",
                "Jaunpur",
                "Jhansi",
                "Kannauj",
                "Kanpur",
                "Lakhimpur",
                "Lalitpur",
                "Lucknow",
                "Mainpuri",
                "Mathura",
                "Meerut",
                "Mirzapur-Vindhyachal",
                "Moradabad",
                "Muzaffarnagar",
                "Partapgarh",
                "Pilibhit",
                "Prayagraj",
                "Rae Bareli",
                "Rampur",
                "Saharanpur",
                "Sambhal",
                "Shahjahanpur",
                "Sitapur",
                "Sultanpur",
                "Tehri",
                "Varanasi",
            ],
            "Uttarakhand": [
                "Almora",
                "Dehra Dun",
                "Haridwar",
                "Mussoorie",
                "Nainital",
                "Pithoragarh",
            ],
            "West Bengal": [
                "Alipore",
                "Alipur Duar",
                "Asansol",
                "Baharampur",
                "Bally",
                "Balurghat",
                "Bankura",
                "Baranagar",
                "Barasat",
                "Barrackpore",
                "Basirhat",
                "Bhatpara",
                "Bishnupur",
                "Budge Budge",
                "Burdwan",
                "Chandernagore",
                "Darjeeling",
                "Diamond Harbour",
                "Dum Dum",
                "Durgapur",
                "Halisahar",
                "Haora",
                "Hugli",
                "Ingraj Bazar",
                "Jalpaiguri",
                "Kalimpong",
                "Kamarhati",
                "Kanchrapara",
                "Kharagpur",
                "Cooch Behar",
                "Kolkata",
                "Krishnanagar",
                "Malda",
                "Midnapore",
                "Murshidabad",
                "Nabadwip",
                "Palashi",
                "Panihati",
                "Purulia",
                "Raiganj",
                "Santipur",
                "Shantiniketan",
                "Shrirampur",
                "Siliguri",
                "Siuri",
                "Tamluk",
                "Titagarh",
            ],
        }

        # Select the state
        state = st.selectbox("Select State", list(state_cities.keys()))

        # Filter cities based on selected state
        selected_cities = state_cities[state]

        # Display dropdown for cities
        city_name = st.selectbox("Select City", selected_cities)

        rooftop = st.text_input("Enter your roof-top area(in sq.feet)")
        shadow = st.text_input("Enter % of shadowed area available")

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

        # Prediction button
        if st.button("Predict", type="secondary"):

            # Display the new rooftop area
            st.write(
                f"<h3 style='color:white;'>Total number of solar panels required after subtracting {shadow_percentage}% shadowed area from total roof top area: {new_rooftop_area_sqft:.2f}</h3>",
                unsafe_allow_html=True,
            )

            # if state == "Maharashtra" or state == "Goa":
            #     # prediction = pred(
            #     #     4461,
            #     #     1795087538,
            #     #     24.7412737999999,
            #     #     23.7866617999999,
            #     #     0.002838054505,
            #     #     65.9333333333333,
            #     # )
            #     # Display predictions
            #     # st.write("Linear Regression Prediction:", lr_prediction[0])
            #     # st.write("Decision Tree Prediction:", dt_prediction[0])
            #     # st.write("Random Forest Prediction:", rf_prediction[0])
            #     # st.write("Average Prediction:", average_prediction[0])
            #     # Round the prediction to 2 decimal places
            #     # rounded_prediction = round(prediction, 2)

            #     # Display the rounded prediction
            #     # st.write(
            #     #     f"<h3 style='color:white;'>Predicted Power generation: {rounded_prediction}W</h3>",
            #     #     unsafe_allow_html=True,
            #     # )
            #     st.write(
            #         f"<h3 style='color:white;'>Predicted Power generation/month:120 units(1 kg)</h3>",
            #         unsafe_allow_html=True,
            #     )
            # elif state == "Rajasthan":
            #     st.write(
            #         "<h3 style='color:white;'>Predicted Power generation/month:127 units(1 kg)</h3>",
            #         unsafe_allow_html=True,
            #     )
            # elif state == "Gujarat":
            #     st.write(
            #         "<h3 style='color:white;'>Predicted Power generation/month:127 units(1 kg)</h3>",
            #         unsafe_allow_html=True,
            #     )
            # elif state == "Delhi":
            #     st.write(
            #         "<h3 style='color:white;'>Predicted Power generation/month:115 units(1 kg)</h3>",
            #         unsafe_allow_html=True,
            #     )
            # elif state == "Jammu and Kashmir":
            #     st.write(
            #         "<h3 style='color:white;'>Predicted Power generation/month:95 units(1 kg)</h3>",
            #         unsafe_allow_html=True,
            #     )
            # elif (
            #     state == "Himachal Pradesh"
            #     or state == "Punjab"
            #     or state == "Chandigarh"
            #     or state == "Uttarakhand"
            # ):
            #     st.write(
            #         "<h3 style='color:white;'>Predicted Power generation/month:110 units(1 kg)</h3>",
            #         unsafe_allow_html=True,
            #     )
            # elif (
            #     state == "Andhra Pradesh"
            #     or state == "Karnataka"
            #     or state == "Kerala"
            #     or state == "Tamil Nadu"
            # ):
            #     st.write(
            #         "<h3 style='color:white;'>Predicted Power generation/month:127 units(1 kg)</h3>",
            #         unsafe_allow_html=True,
            #     )
            # elif (
            #     state == "Uttar Pradesh"
            #     or state == "Bihar"
            #     or state == "Jharkhand"
            #     or state == "Madhya Pradesh"
            # ):
            #     st.write(
            #         "<h3 style='color:white;'>Predicted Power generation/month:122 units(1 kg)</h3>",
            #         unsafe_allow_html=True,
            #     )
            # else:
            #     st.write(
            #         "<h3 style='color:white;'>Predicted Power generation/month:120 units(1 kg)</h3>",
            #         unsafe_allow_html=True,
            #     )

            # st.write(
            #     "<h3 style='color:white;'>There are 2 major varieties available:</h3>",
            #     unsafe_allow_html=True,
            # )
            # st.write(
            #     "<h5 style='color:white;'>Rs. 18,000 is for solar panels which generate 550 Watt of electricity and weight is around 28kg.</h5>",
            #     unsafe_allow_html=True,
            # )
            # st.write(
            #     "<h5 style='color:white;'>Rs. 11,500 is for solar panels which generate 350 Watt of electricity and weight is around 28kg.</h5>",
            #     unsafe_allow_html=True,
            # )
            # st.write(
            #     "<h5 style='color:white;font-size:27px;'>For further inquiry, Contact: <a href='tel:+919422161101'>+91 94221 61101</a></h5>",
            #     unsafe_allow_html=True,
            # )

            if city_name:
                # weather_data = get_weather(city_name)

                # if weather_data:
                    # st.write("Weather Data:")
                    # st.write(weather_data)

                    # Extract latitude and longitude
                    # if "coord" in weather_data:
                    #     lat = weather_data["coord"]["lat"]
                    #     lon = weather_data["coord"]["lon"]
                    #     # st.write(f"Latitude: {lat}, Longitude: {lon}")

                    # else:
                    #     st.write("Latitude and longitude not found in response.")

                    weather_history = get_weather_history(city_name)

                    if weather_history:
                        # st.write("Weather History Data:")
                        # st.write(weather_history)
                        print("Weather history")
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
                    # st.write(Temp_array)

                    # New array for sunlight hours
                    sunlight_hrs = []
                    # Iterate over the temperature array
                    for t in Temp_array:
                        if t < 30:
                            sunlight_hrs.append(round(9 + 0.5 * (t - 30), 2))
                        else:
                            sunlight_hrs.append(round(10 + (t - 30), 2))

                    # Printing the sunlight hours array
                    # st.write(sunlight_hrs)
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
                    # st.write("Predicted Power Generation/month:")
                    # st.write(predictions_per_month)

                    # Calculate sum of predictions per month
                    total_predictions = sum(predictions_per_month)
                    average_total_predictions_per_month = total_predictions / 12

                    # Display sum
                    st.write(
                        f"<h3 style='color:white;'>Average Power Generation/month(per panel):{average_total_predictions_per_month:.2f} units.</h3>",
                        unsafe_allow_html=True,
                    )

                    # Multiply total predictions by new rooftop area
                    total_energy_generation = total_predictions * new_rooftop_area_sqft
                    average_energy_generation_per_month = total_energy_generation / 12

                    # Display total energy generation
                    st.write(
                        f"<h3 style='color:white;'>Average Solar Power Generation/month:{average_energy_generation_per_month:.2f} units.</h3>",
                        unsafe_allow_html=True,
                    )

                    # Generate some example month names for the x-axis
                    month_names = [
                        "Jan",
                        "Feb",
                        "Mar",
                        "Apr",
                        "May",
                        "Jun",
                        "Jul",
                        "Aug",
                        "Sep",
                        "Oct",
                        "Nov",
                        "Dec",
                    ]

                    # Create a Plotly figure
                    fig = go.Figure()

                    # Add a trace for the predictions
                    fig.add_trace(
                        go.Scatter(
                            x=month_names,
                            y=predictions_per_month,
                            mode="lines",
                            name="Predictions",
                        )
                    )

                    # Update layout with titles and axis labels
                    fig.update_layout(
                        title=f"Predicted Power Generation/month for {city_name}",
                        xaxis_title="Month",
                        yaxis_title="Power Generation",
                        showlegend=True,
                        xaxis=dict(
                            tickmode="array",
                            tickvals=list(range(len(month_names))),
                            ticktext=month_names,
                        ),
                        yaxis=dict(gridcolor="lightgrey"),
                        height=700,  # Adjust the height as needed
                        width=1500,  # Adjust the width as needed
                        margin=dict(
                            t=50, b=50, l=50, r=50
                        ),  # Adjust margins to center-align the plot
                        font=dict(size=34),  # Adjust font size
                    )

                    # Show the plot
                    st.plotly_chart(fig)
                # else:
                #     st.write(
                #         "Failed to fetch weather data. Please check your input and try again."
                #     )
            else:
                st.write("Please enter both city name and API key.")

    else:
        st.text("Please Login first")


if __name__ == "__main__":
    main()
