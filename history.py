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


# Initialize Firebase
# cred = credentials.Certificate("fy-project-a9188-c7e54655ad87.json")
# print(cred)
# firebase_admin.initialize_app(cred)
db = firestore.client()


# Load the trained models
model1 = load_model("C:/FY_Project/vgg_new.hdf5", compile=False)
model2 = load_model("C:/FY_Project/resnet50_new.hdf5", compile=False)
model3 = load_model("C:/FY_Project/mobilenetv3_new.hdf5", compile=False)


def display_defect_card(defect, logged_in_username):
    if defect["username"] == logged_in_username:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 3, 3])
        with col1:
            # st.image("", width=1)  # Adjust spacing

            pass
        with col2:
            st.write(f"**Username:** {defect['username']}")
            st.write(f"**Defect Class:** {defect['defect_class']}")
        with col3:
            try:
                image_bytes = base64.b64decode(defect["image"])
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="Uploaded Image", width=300)
            except Exception as e:
                st.error("Error loading image: {}".format(e))
        st.markdown("---")


# Streamlit app
def main():
    st.title("Previous History")

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
