import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
from collections import Counter
import io
import base64
import firebase_admin
from keras.models import load_model
from firebase_admin import credentials, firestore, initialize_app, storage


# Initialize Firebase
# cred = credentials.Certificate("fy-project-a9188-c7e54655ad87.json")
# print(cred)
# firebase_admin.initialize_app(cred)
if not firebase_admin._apps:
    # Initialize Firebase
    cred = credentials.Certificate("fy-project-a9188-c7e54655ad87.json")
    # print(cred)
    firebase_admin.initialize_app(cred)

db = firestore.client()


# Streamlit app
def main():
    st.title("Goverment Schemes")

    if st.session_state.username != "":
        st.write(
            "<div style='color: white;font-weight:500;font-size:37px;margin-bottom:7px;'><b><i>Steps to apply for rooftop solar:</i></b></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:25px;margin-bottom:7px;margin:5px;'>Step 1. Register in the portal with the following:<ul ><li>Select your State</li><li>Select your District</li><li>Select Electricity Distribution Company</li><li>Enter your Consumer Account Number</li><li>Enter Mobile</li></ul></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:25px;margin-bottom:7px;margin:5px;'>Step 2. Login:<ul><li>Login with Mobile Number</li><li>Apply for the Rooftop</li></ul></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:25px;margin-bottom:7px;margin:5px;'>Step 3. Once you get the feasibility approval, get the plant installed by any of the registered vendors in your DISCOM.</div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:25px;margin-bottom:7px;margin:5px;'>Step 4. Once installation is completed, submit the plant details and apply for net meter.</div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:25px;margin-bottom:7px;margin:5px;'>Step 5. Commissioning certificate will be generated from the portal, after installation of net meter and inspection by DISCOM.</div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:25px;margin-bottom:7px;margin-bottom:10px;'>Step 6. Once you get the commissioning report. Submit the bank account details and a cancelled cheque through the portal. You will receive your subsidy in your bank account within 30 days.</div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:500;font-size:25px;margin-bottom:7px;'><b><i>Click here to apply:<a style='color:blue;padding-left:10px;' href='https://www.pmsuryaghar.gov.in/'>https://www.pmsuryaghar.gov.in/</a></i></b></div>",
            unsafe_allow_html=True,
        )
    else:
        st.text("Please Login first")


if __name__ == "__main__":
    main()
