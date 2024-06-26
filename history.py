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

class_names = [
    "Bird-drop",
    "Clean",
    "Dusty",
    "Electrical-damage",
    "Physical-Damage",
    "Snow-Covered",
]

button_styles = """
    <style>
        .css-16idsys p {
            margin-bottom: 0px;
            font-size: 35px;
            color: #FFFFFF;
            font-weight: bolder;
            margin-top: -30px;
        }
        .css-5rimss p {
            word-break: break-word;
            color: #FFFFFF;
            font-size: 35px;
            font-weight: bolder;
            margin-bottom: -10px;
            margin-top: -60px;
        }

        .css-10trblm.eqr7zpz0 {
            color: #FFFFFF;
            font-size:40px
        }
        element.style {
            margin-left: 15px;
            color: white;
            font-weight: bolder;
            font-size: 30px;
            margin-bottom: 7px;
            margin-left: -1px;
        }
        .css-1uixxvy {
            margin-right: 0.5rem;
            margin-bottom: 0.25rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-size: 30px;
            color: #FFFFFF;
        }
        .css-1y4p8pa{
            max-width:none;
            padding-left:7rem;
            padding-top:0px;
        }
        [data-testid="stAppViewContainer"] > .main{
            background-image: url(data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxISEhUSEhIVFRUVFxcVFxcXFxcaFxcVFRcXFxUXFRcYHSggGBolHRUXITEiJSkrLi4uFx8zODMtNygtLisBCgoKDQ0NDg0NDisZFRk3LSsrNysrKystKy0rKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrK//AABEIALcBEwMBIgACEQEDEQH/xAAYAAEBAQEBAAAAAAAAAAAAAAACAQADB//EAB4QAQEBAQEAAgMBAAAAAAAAAAABEQISgfBRcZEx/8QAFgEBAQEAAAAAAAAAAAAAAAAAAAEC/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8A8oirFVlIrSFgJFxcWQExYuKCYshYuAmNIUi4A4vlauAmNiz/AFcAcXFkXAHGwkAbEw8TACxsPEBzxrDxMAKNPEoOeMViWAI0sYBSwkAWXGAoyQpAWLEhA2FGiyA0irFgJhSNIsgNIsi4oCuLiyAMWFi+RRxsLGwBawsawAxsPEwAsSw8QQLEsPBsALBp2JYAYNOpQAcMaA1KVggjMoKuKsBoUSHAZY0hYDRcWRZAWRY0iwGxrFYElKMUBFnK+SkFGoWNgDIxWNYAISAKWFiWCDRq1KAjTTACwa6WBQBCqUBsGlUqg6rMgUXEiqFCGQ5EFhRIsAljSLAUh5OA0WxlAcJcXmAkhRJFBlxVooWIeJQCxCqCA1WpQCpYSANiWQrBoDYFOjQCxKVg1QEp0QHGVgJtTkoCylEixA+aXIwpAKLBKAUKDCgKUEgZcZQbFitgqFUiwGqWENEGxFSgKUhAaNKoAotQBGmFAaNLoelBRaNBmT5YFhJCgLF5aKgpRIUAosiQoCw5BhQFVFgFixIUoKuDDgo2LKrUEGlI1EBsKjoDg0hoDaNKwbAQaVAEqUqFBKNIaoNg0qNAWZgKFAhwChQIcqBQoBQChhDgLiz9soLFgrAOLBigcUdWASprCqKpREsFfv38pQTBpYNAaNMKA0aVGgKVbEoDRtKwaoNGlRoIyMCw4EIChQIUqBwoEOAUKDFlA4UDS0C1aOrAUkSAcXQ1dA5W9C2gUa1NS0FtBalBEtaoDC1S0EoqNBKJDVBSrUoDRxUoJ/WZgaLBhQChQYsA10YUQItDSgHKQRYBtEUCiwC5oLF0WgEQ6loHo2po2gWoyaC2ilTQa0dWoCUV1LQSi1qKNRq9BQbRq6lBGZgQhXQOFHOFED1eQhyAcUSlBdXRlWAfJSucq6DpqyufJSgbaHprQPWGVAJrR1qBDqa2g2o2pQYda1NBhtbUtUZEsQGo2tUoMlSNQTWRgZZRiygUpQJSiDpysoRYocLXOUpUDjDKsoEsFQIvQa0oHKwxgPW0dTQNNRtBWHWBqlbR0GStRqi1KkTQa1K2paCI1qUGqVKwN8smsCKzILqxmAtWVmAljMoq6zAsVmQXVlZgW9NazAkrarA2pemYG1tZlBvQyswMjMCaNrMCVKzAmozAw2swJjMwP//Z);
            background-size: 100vw 100vh;
            background-repeat: no-repeat;
        }
    </style>
"""


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


# Load the trained models
model1 = load_model("C:/FY_Project/vgg_new.hdf5", compile=False)
model2 = load_model("C:/FY_Project/resnet50_new.hdf5", compile=False)
model3 = load_model("C:/FY_Project/mobilenetv3_new.hdf5", compile=False)


def display_defect_card(defect, logged_in_username):
    if defect["username"] == logged_in_username:

        # Add horizontal rule
        st.markdown("------------------------")
        col2, col3 = st.columns([6, 3])

        with col2:
            st.write(
                "<div style='color:white;text-decoration:underline;'><h2>Detected Defect:</h2></div>",
                unsafe_allow_html=True,
            )
            st.write(
                f"<div style='margin-left: 15px; color: white;font-weight:500;font-size:30px; margin-bottom:7px;'><b><i>{defect['defect_class']}</i></b></div>",
                unsafe_allow_html=True,
            )
            if defect["defect_class"] == "Physical-Damage":
                st.write(
                    "<div style='color:white;text-decoration:underline;'><h2>Defect Description:</h2></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:30px;margin-bottom:7px;'><b><i>Physical damage refers to any kind of harm or impairment to the solar panel structure or components caused by external forces.</i></b></div>",
                    unsafe_allow_html=True,
                )

                st.write(
                    "<div style='color:white;text-decoration:underline;'><h2>Remedies:</h2></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:30px;'><b><i>If a solar panel is physically damaged, it will need to be replaced.</i></b></div>",
                    unsafe_allow_html=True,
                )
            elif defect["defect_class"] == "Snow-Covered":
                st.write(
                    "<div style='color:white;text-decoration:underline;'><h2>Defect Description:</h2></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:30px;margin-bottom:7px;'><b><i>Snow accumulation on solar panels can significantly reduce their energy production.</i></b></div>",
                    unsafe_allow_html=True,
                )

                st.write(
                    "<div style='color:white;text-decoration:underline;'><h2>Remedies:</h2></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:30px;'><b><i>If there is a lot of snow, it may be necessary to remove it manually.</i></b></div>",
                    unsafe_allow_html=True,
                )
            elif defect["defect_class"] == "Electrical-damage":
                st.write(
                    "<div style='color:white;text-decoration:underline;'><h2>Defect Description:</h2></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:30px;margin-bottom:7px;'><b><i>Electrical damage involves faults or malfunctions in the electrical components of the solar panel system.</i></b></div>",
                    unsafe_allow_html=True,
                )

                st.write(
                    "<div style='color:white;text-decoration:underline;'><h2>Remedies:</h2></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:30px;'><b><i>If a solar panel is damaged by electrical damage, it will need to be replaced.</i></b></div>",
                    unsafe_allow_html=True,
                )
            elif defect["defect_class"] == "Dusty":
                st.write(
                    "<div style='color:white;text-decoration:underline;'><h2>Defect Description:</h2></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:30px;;margin-bottom:7px;'><b><i>Dust and dirt particles settle on the surface of the panels, blocking sunlight and reducing the amount of light absorbed by the photovoltaic cells.</i></b></div>",
                    unsafe_allow_html=True,
                )

                st.write(
                    "<div style='color:white;text-decoration:underline;'><h2>Remedies:</h2></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:30px;'><b><i>It is important to clean solar panels regularly to remove any dirt or debris that has accumulated.</i></b></div>",
                    unsafe_allow_html=True,
                )
            elif defect["defect_class"] == "Bird-drop":
                st.write(
                    "<div style='color:white;text-decoration:underline;'><h2>Defect Description:</h2></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:30px;;margin-bottom:7px;'><b><i>Bird droppings or bird poop can land on the surface of solar panels and create shading or soiling issues.</i></b></div>",
                    unsafe_allow_html=True,
                )

                st.write(
                    "<div style='color:white;text-decoration:underline;'><h2>Remedies:</h2></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:30px;'><b><i>It is important to clean bird droppings off of solar panels as soon as possible.</i></b></div>",
                    unsafe_allow_html=True,
                )
        with col3:
            try:
                image_bytes = base64.b64decode(defect["image"])
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="Uploaded Image", width=400)
            except Exception as e:
                st.error("Error loading image: {}".format(e))
        st.markdown("---")


# Streamlit app
def main():
    st.title("Previous History")
    st.markdown(button_styles, unsafe_allow_html=True)

    if st.session_state.username != "":
        # st.header("Recent Defects")
        logged_in_username = st.session_state.username
        defects_ref = db.collection("defects")
        defects_data = defects_ref.get()

        for defect_doc in defects_data:
            defect = defect_doc.to_dict()
            display_defect_card(defect, logged_in_username)

    else:
        st.text("Please Login first")


if __name__ == "__main__":
    main()
