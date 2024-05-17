import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests


# Check if Firebase app is not already initialized
if not firebase_admin._apps:
    # Initialize Firebase
    cred = credentials.Certificate("fy-project-a9188-c7e54655ad87.json")
    # print(cred)
    firebase_admin.initialize_app(cred)
db = firestore.client()


def app():

    # Usernm = []
    st.title("Solar Panel Defect Detection using Computer Vision")

    if "username" not in st.session_state:
        st.session_state.username = ""
    if "useremail" not in st.session_state:
        st.session_state.useremail = ""

    def sign_up_with_email_and_password(
        email, password, username=None, return_secure_token=True
    ):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token,
            }
            if username:
                payload["displayName"] = username
            payload = json.dumps(payload)
            r = requests.post(
                rest_api_url,
                params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"},
                data=payload,
            )
            users_ref = db.collection("users")
            users_ref.add({"email": email, "password": password, "username": username})
            try:
                return r.json()["email"]
            except:
                st.warning(r.json())
        except Exception as e:
            st.warning(f"Signup failed: {e}")

    def sign_in_with_email_and_password(
        email=None, password=None, return_secure_token=True
    ):
        rest_api_url = (
            "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        )

        try:
            payload = {"returnSecureToken": return_secure_token}
            if email:
                payload["email"] = email
            if password:
                payload["password"] = password
            payload = json.dumps(payload)
            # print('payload sigin',payload)
            r = requests.post(
                rest_api_url,
                params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"},
                data=payload,
            )
            try:
                data = r.json()
                user_info = {
                    "email": data["email"],
                    "username": data.get(
                        "displayName"
                    ),  # Retrieve username if available
                }
                return user_info
            except:
                st.warning(data)
        except Exception as e:
            st.warning(f"Signin failed: {e}")

    def f():
        try:
            # user = auth.get_user_by_email(email)
            # print(user.uid)
            # st.session_state.username = user.uid
            # st.session_state.useremail = user.email

            userinfo = sign_in_with_email_and_password(
                st.session_state.email_input, st.session_state.password_input
            )
            st.session_state.username = userinfo["username"]
            st.session_state.useremail = userinfo["email"]

            global Usernm
            Usernm = userinfo["username"]

            st.session_state.signedout = True
            st.session_state.signout = True

        except:
            st.warning("Login Failed")

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ""

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if "signout" not in st.session_state:
        st.session_state["signout"] = False

    if not st.session_state[
        "signedout"
    ]:  # only show if the state is False, hence the button has never been clicked
        choice = st.selectbox("Login/Signup", ["Login", "Sign up"])
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        st.session_state.email_input = email
        st.session_state.password_input = password

        if choice == "Sign up":
            username = st.text_input("Enter  your unique username")

            if st.button("Create my account"):
                # user = auth.create_user(email = email, password = password,uid=username)
                user = sign_up_with_email_and_password(
                    email=email, password=password, username=username
                )

                st.success("Account created successfully!")
                st.markdown("Please Login using your email and password")
                st.balloons()
        else:
            # st.button('Login', on_click=f)
            st.button("Login", on_click=f)

    if st.session_state.signout:
        # st.text("Username: " + st.session_state.username)
        st.write("Welcome " + st.session_state.username + ", ")
        st.write(
            "<div style='color: black;font-weight:600!important;font-size:35px;margin-bottom:30%;'><i style='text-decoration:underline;color:white;font-weight:700;'>Problem Statement:</i><b> Manual inspection of solar panels is time-consuming and expensive. Therefore, our automated system utilizes computer vision techniques to accurately identify and classify defects in solar panels which is required to improve maintenance efficiency and ensure optimal energy generation from solar installations.</b></div>",
            unsafe_allow_html=True,
        )
        

        # st.text("Email-id: " + st.session_state.useremail)
        st.button("Log out", on_click=t)

    def ap():
        st.write("Posts")
