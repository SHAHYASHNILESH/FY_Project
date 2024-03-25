import streamlit as st
from firebase_admin import firestore

# def app():
    
#     if 'db' not in st.session_state:
#         st.session_state.db = ''

#     db=firestore.client()
#     st.session_state.db=db
#     # st.title('  :violet[Pondering]  :sunglasses:')
    
#     ph = ''
#     if st.session_state.username=='':
#         ph = 'Login to be able to post!!'
#     else:
#         ph='Post your thought'    
#     post=st.text_area(label=' :orange[+ New Post]',placeholder=ph,height=None, max_chars=500)
#     if st.button('Post',use_container_width=20):
#         if post!='':
                    
#             info = db.collection('Posts').document(st.session_state.username).get()
#             if info.exists:
#                 info = info.to_dict()
#                 if 'Content' in info.keys():
                
#                     pos=db.collection('Posts').document(st.session_state.username)
#                     pos.update({u'Content': firestore.ArrayUnion([u'{}'.format(post)])})
#                     # st.write('Post uploaded!!')
#                 else:
                    
#                     data={"Content":[post],'Username':st.session_state.username}
#                     db.collection('Posts').document(st.session_state.username).set(data)    
#             else:
                    
#                 data={"Content":[post],'Username':st.session_state.username}
#                 db.collection('Posts').document(st.session_state.username).set(data)
                
#             st.success('Post uploaded!!')
    
#     st.header(' :violet[Latest Posts] ')
    
    
    
    
    
#     docs = db.collection('Posts').get()
            
#     for doc in docs:
#         d=doc.to_dict()
#         try:
#             st.text_area(label=':green[Posted by:] '+':orange[{}]'.format(d['Username']),value=d['Content'][-1],height=20)
#         except: pass


import streamlit as st
import tensorflow as tf
from PIL import Image
from keras.models import load_model
import numpy as np

class_names=['Bird-drop', 'Clean', 'Dusty', 'Electrical-damage', 'Physical-Damage', 'Snow-Covered']

# Load the trained models
model1 = load_model('C:/FY_Project/vgg_new.hdf5',compile=False)
model2 = load_model('C:/FY_Project/resnet50_new.hdf5',compile=False)
model3 = load_model('C:/FY_Project/mobilenetv3_new.hdf5',compile=False)

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
