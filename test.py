import streamlit as st
import tensorflow as tf
from PIL import Image
from keras.models import load_model
import numpy as np

class_names=['Bird-drop', 'Clean', 'Dusty', 'Electrical-damage', 'Physical-Damage', 'Snow-Covered']

# Load the trained models
model1 = load_model('C:/pondering/vgg_new.hdf5',compile=False)
model2 = load_model('C:/pondering/resnet50_new.hdf5',compile=False)
model3 = load_model('C:/pondering/mobilenetv3_new.hdf5',compile=False)

# Preprocessing function
def preprocess_image(image):
    # Resize the image to match the input size of the models
    image = image.resize((224, 224))
    # Convert image to numpy array
    image = np.array(image)

    # Expand dimensions to match the input shape of the models
    image = np.expand_dims(image, axis=0)
    return image

# Define defect detection function
def detect_defect(image,name):
    image = preprocess_image(image)
    # Predict using each model
    if name=='VGG':
        prediction = model1.predict(image)
    elif name=='Resnet':
        prediction = model2.predict(image)
    else:
        prediction = model3.predict(image)
    # prediction2 = model2.predict(image)
    # prediction3 = model3.predict(image)
    # Combine predictions
    # combined_prediction = (prediction1 + prediction2 + prediction3) / 3.0
    # return combined_prediction
    return prediction


# Streamlit app
def main():
    st.title('Solar Panel Defect Detection')
    st.write('Upload an image of a solar panel to detect defects.')

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Detect defect
        prediction1 = detect_defect(image,'VGG')
        st.write(prediction1)
        score1 = tf.nn.softmax(prediction1[0])

        prediction2 = detect_defect(image,'Resnet')
        st.write(prediction2)
        score2 = tf.nn.softmax(prediction2[0])

        prediction3 = detect_defect(image,'Mobilenet')
        st.write(prediction3)
        score3 = tf.nn.softmax(prediction3[0])
        
        # Display result
        st.write('Defect Class from VGG-Model:', class_names[np.argmax(score1)])
        st.write('Defect Class from Resnet-50 Model:', class_names[np.argmax(score2)])
        st.write('Defect Class from MobileNetV3 Model:', class_names[np.argmax(score3)])


main()
