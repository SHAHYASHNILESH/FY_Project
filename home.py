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


# Preprocessing function
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    return image


# Define defect detection function
def detect_defect(image, name):
    image = preprocess_image(image)
    if name == "VGG":
        prediction = model1.predict(image)
    elif name == "Resnet":
        prediction = model2.predict(image)
    else:
        prediction = model3.predict(image)
    return prediction


def display_defect_card(defect):
    print(defect["username"])
    col1, col2, col3 = st.columns([1, 3, 3])
    with col1:
        print("aa")
        # st.image("", width=1)  # Adjust spacing
    with col2:
        st.write(f"**Username:** {defect['username']}")
        st.write(f"**Defect Class:** {defect['defect_class']}")
    with col3:
        try:
            image_bytes = base64.b64decode(defect["image"])
            # print(image_bytes)
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption="Uploaded Image", use_column_width=True)
        except Exception as e:
            st.error("Error loading image: {}".format(e))


# Streamlit app
def main():
    st.title("Solar Panel Defect Detection")

    if st.session_state.username != "":
        st.write("Upload an image of a solar panel to detect defects.")
        uploaded_file = st.file_uploader(
            "Choose an image..", type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Detect defect
            prediction1 = detect_defect(image, "VGG")
            score1 = tf.nn.softmax(prediction1[0])
            prediction2 = detect_defect(image, "Resnet")
            score2 = tf.nn.softmax(prediction2[0])
            prediction3 = detect_defect(image, "Mobilenet")
            score3 = tf.nn.softmax(prediction3[0])

            index1 = np.argmax(score1)
            index2 = np.argmax(score2)
            index3 = np.argmax(score3)

            combined_indices = [index1, index2, index3]
            vote_count = Counter(combined_indices)
            majority_index = vote_count.most_common(1)[0][0]
            majority_class_name = class_names[majority_index]

            # print(uploaded_file)
            st.write("Defect Detected:", majority_class_name)

            # Store image and defect in Firestore
            if st.button("Send to Manager"):
                with io.BytesIO() as output:
                    image.save(output, format="JPEG")
                    image_bytes = output.getvalue()
                image_b64 = base64.b64encode(image_bytes).decode()
                defects_ref = db.collection("defects")
                defects_ref.add(
                    {
                        "username": st.session_state.username,
                        "image": image_b64,
                        "defect_class": majority_class_name,
                    }
                )
                st.success("Image and defect sent successfully!")

    else:
        st.text("Please Login first")


if __name__ == "__main__":
    main()
