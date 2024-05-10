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

button_styles = """
    <style>
        # .css-5rimss li {
        #     margin: 0.2em 0px 0.2em 1.2em;
        #     padding: 0px 0px 0px 0.6em;
        #     font-size: 1rem;
        #     font-size: 28px;
        #     font-weight: bolder;
        # }
        # .css-1n76uvr {
        #     width: 704px;
        #     position: relative;
        #     display: flex;
        #     flex: 1 1 0%;
        #     flex-direction: column;
        #     gap: 1rem;
        #     margin-left: -600px;
        #     margin-top: -120px;
        # }
        .css-1y4p8pa{
            max-width:none;
            padding-left:7rem;
            padding-top:0px;
        }

        .css-nahz7x li{
            font-size:30px;
        }

        [data-testid="stAppViewContainer"] > .main {
            background-image: url(data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxISEhUSEhIVFRUVFxcVFxcXFxcaFxcVFRcXFxUXFRcYHSggGBolHRUXITEiJSkrLi4uFx8zODMtNygtLisBCgoKDQ0NDg0NDisZFRk3LSsrNysrKystKy0rKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrK//AABEIALcBEwMBIgACEQEDEQH/xAAYAAEBAQEBAAAAAAAAAAAAAAACAQADB//EAB4QAQEBAQEAAgMBAAAAAAAAAAABEQISgfBRcZEx/8QAFgEBAQEAAAAAAAAAAAAAAAAAAAEC/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8A8oirFVlIrSFgJFxcWQExYuKCYshYuAmNIUi4A4vlauAmNiz/AFcAcXFkXAHGwkAbEw8TACxsPEBzxrDxMAKNPEoOeMViWAI0sYBSwkAWXGAoyQpAWLEhA2FGiyA0irFgJhSNIsgNIsi4oCuLiyAMWFi+RRxsLGwBawsawAxsPEwAsSw8QQLEsPBsALBp2JYAYNOpQAcMaA1KVggjMoKuKsBoUSHAZY0hYDRcWRZAWRY0iwGxrFYElKMUBFnK+SkFGoWNgDIxWNYAISAKWFiWCDRq1KAjTTACwa6WBQBCqUBsGlUqg6rMgUXEiqFCGQ5EFhRIsAljSLAUh5OA0WxlAcJcXmAkhRJFBlxVooWIeJQCxCqCA1WpQCpYSANiWQrBoDYFOjQCxKVg1QEp0QHGVgJtTkoCylEixA+aXIwpAKLBKAUKDCgKUEgZcZQbFitgqFUiwGqWENEGxFSgKUhAaNKoAotQBGmFAaNLoelBRaNBmT5YFhJCgLF5aKgpRIUAosiQoCw5BhQFVFgFixIUoKuDDgo2LKrUEGlI1EBsKjoDg0hoDaNKwbAQaVAEqUqFBKNIaoNg0qNAWZgKFAhwChQIcqBQoBQChhDgLiz9soLFgrAOLBigcUdWASprCqKpREsFfv38pQTBpYNAaNMKA0aVGgKVbEoDRtKwaoNGlRoIyMCw4EIChQIUqBwoEOAUKDFlA4UDS0C1aOrAUkSAcXQ1dA5W9C2gUa1NS0FtBalBEtaoDC1S0EoqNBKJDVBSrUoDRxUoJ/WZgaLBhQChQYsA10YUQItDSgHKQRYBtEUCiwC5oLF0WgEQ6loHo2po2gWoyaC2ilTQa0dWoCUV1LQSi1qKNRq9BQbRq6lBGZgQhXQOFHOFED1eQhyAcUSlBdXRlWAfJSucq6DpqyufJSgbaHprQPWGVAJrR1qBDqa2g2o2pQYda1NBhtbUtUZEsQGo2tUoMlSNQTWRgZZRiygUpQJSiDpysoRYocLXOUpUDjDKsoEsFQIvQa0oHKwxgPW0dTQNNRtBWHWBqlbR0GStRqi1KkTQa1K2paCI1qUGqVKwN8smsCKzILqxmAtWVmAljMoq6zAsVmQXVlZgW9NazAkrarA2pemYG1tZlBvQyswMjMCaNrMCVKzAmozAw2swJjMwP//Z);
            background-size: 100vw 100vh;
            background-repeat: no-repeat;
        }
    </style>
"""

# background_image = """
# <style>
# [data-testid="stAppViewContainer"] > .main {
#     background-image: url("https://png.pngtree.com/thumb_back/fh260/back_our/20190620/ourmid/pngtree-gradient-silhouette-people-s-name-government-board-poster-background-material-image_144469.jpg");
#     background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
#     background-position: center;
#     background-repeat: no-repeat;
# }
# </style>
# # """


# Streamlit app
def main():
    st.markdown(button_styles, unsafe_allow_html=True)
    # st.markdown(background_image, unsafe_allow_html=True)

    st.title("Government Schemes")

    if st.session_state.username != "":
        st.write(
            "<div style='color: white;font-weight:600;font-size:35px;margin-bottom:7px;'><b><i>Steps to apply for rooftop solar:</i></b></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:30px;margin-bottom:7px;margin:5px;'>Step 1. Register in the portal with the following:<ul ><li>Select your State</li><li>Select your District</li><li>Select Electricity Distribution Company</li><li>Enter your Consumer Account Number</li><li>Enter Mobile</li></ul></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:30px;margin-bottom:7px;margin:5px;'>Step 2. Login:<ul><li>Login with Mobile Number</li><li>Apply for the Rooftop</li></ul></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:28px;margin-bottom:7px;margin:5px;'>Step 3. Once you get the feasibility approval, get the plant installed by any of the registered vendors in you DISCOM.</div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:28px;margin-bottom:7px;margin:5px;'>Step 4. Once installation is completed, submit the plant details and apply for net meter.</div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:28px;margin-bottom:7px;margin:5px;'>Step 5. Commissioning certificate will be generated from the portal, after installation of net meter and inspection by DISCOM.</div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:28px;margin-bottom:7px;margin-bottom:10px;'>Step 6. Once you get the commissioning report. Submit the bank account details and a cancelled cheque through the portal. You will receive your subsidy in your bank account within 30 days.</div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='color: white;font-weight:600;font-size:28px;margin-bottom:7px;'><b><i>Click here to apply:<a style='color:blue;padding-left:10px;' href='https://www.pmsuryaghar.gov.in/'>https://www.pmsuryaghar.gov.in/</a></i></b></div>",
            unsafe_allow_html=True,
        )
    else:
        st.text("Please Login first")


if __name__ == "__main__":
    main()
