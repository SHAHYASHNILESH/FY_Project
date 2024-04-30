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
        st.write("Upload an image of solar panel to detect defects.")
        uploaded_file = st.file_uploader(
            "Choose an image:", type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", width=400)
            

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
            st.write("<div style='color:white;text-decoration:underline;'><h5>Defect Detected:</h5></div><div style='margin-left: 15px; color: white;font-weight:500;font-size:18px;margin-bottom:7px;'>{}</div>".format(majority_class_name), unsafe_allow_html=True)

            if majority_class_name == "Physical-Damage":
                st.write(
                    "<div style='color:white;text-decoration:underline;'><h5>Defect Description:</h5></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:18px;margin-bottom:7px;'><b><i>Physical damage refers to any kind of harm or impairment to the solar panel structure or components caused by external forces.</i></b></div>",
                    unsafe_allow_html=True,
                )

                st.write(
                    "<div style='color:white;text-decoration:underline;'><h5>Reparation Suggestion:</h5></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:18px;;margin-bottom:5px;'><b><i>If a solar panel is physically damaged, it will need to be repaired or replaced.</i></b></div>",
                    unsafe_allow_html=True,
                )
            
            elif majority_class_name == "Electrical-damage":
                st.write(
                    "<div style='color:white;text-decoration:underline;'><h5>Defect Description:</h5></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:18px;margin-bottom:7px;'><b><i>Electrical damage involves faults or malfunctions in the electrical components of the solar panel system.</i></b></div>",
                    unsafe_allow_html=True,
                )

                st.write(
                    "<div style='color:white;text-decoration:underline;'><h5>Reparation Suggestion:</h5></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:18px;;margin-bottom:5px;'><b><i>If a solar panel is damaged by electrical damage, it will need to be repaired or replaced.</i></b></div>",
                    unsafe_allow_html=True,
                )
            
            elif majority_class_name == "Dusty":
                st.write(
                    "<div style='color:white;text-decoration:underline;'><h5>Defect Description:</h5></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:18px;;margin-bottom:7px;'><b><i>Dust and dirt particles settle on the surface of the panels, blocking sunlight and reducing the amount of light absorbed by the photovoltaic cells.</i></b></div>",
                    unsafe_allow_html=True,
                )

                st.write(
                    "<div style='color:white;text-decoration:underline;'><h5>Reparation Suggestion:</h5></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:18px;;margin-bottom:5px;'><b><i>It is important to clean solar panels regularly to remove any dirt or debris that has accumulated.</i></b></div>",
                    unsafe_allow_html=True,
                )
            elif majority_class_name == "Bird-drop":
                st.write(
                    "<div style='color:white;text-decoration:underline;'><h5>Defect Description:</h5></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:18px;;margin-bottom:7px;'><b><i>Bird droppings or bird poop can land on the surface of solar panels and create shading or soiling issues.</i></b></div>",
                    unsafe_allow_html=True,
                )

                st.write(
                    "<div style='color:white;text-decoration:underline;'><h5>Reparation Suggestion:</h5></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:18px;;margin-bottom:5px;'><b><i>It is important to clean bird droppings off of solar panels as soon as possible.</i></b></div>",
                    unsafe_allow_html=True,
                )
            
            elif majority_class_name == "Snow-Covered":
                st.write(
                    "<div style='color:white;text-decoration:underline;'><h5>Defect Description:</h5></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:18px;margin-bottom:7px;'><b><i>Snow accumulation on solar panels can significantly reduce their energy production.</i></b></div>",
                    unsafe_allow_html=True,
                )

                st.write(
                    "<div style='color:white;text-decoration:underline;'><h5>Reparation Suggestion:</h5></div>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "<div style='margin-left: 15px; color: white;font-weight:500;font-size:18px;margin-bottom:5px;'><b><i>If there is a lot of snow, it may be necessary to remove it manually.</i></b></div>",
                    unsafe_allow_html=True,
                )

            # Store image and defect in Firestore
            if st.button("Save"):
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
                st.success("Image and Defect saved successfully!")

    else:
        st.text("Please Login first")


if __name__ == "__main__":
    main()
