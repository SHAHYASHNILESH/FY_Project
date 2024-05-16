import streamlit as st
import home
import input
import account
import history
import govscheme
from firebase_admin import credentials, firestore, initialize_app, storage

# if not firebase_admin._apps:
#     # Initialize Firebase
#     cred = credentials.Certificate("fy-project-a9188-c7e54655ad87.json")
#     # print(cred)
#     firebase_admin.initialize_app(cred)

# db = firestore.client()

# Define CSS styles for buttons and hover effects
button_styles = """
    <style>
        button[kind="primary"] {
            background:#B4B4B8;
            text-align:left;
            color:black;
            width:100%;
            border: 3px solid black;
            border-radius: 15px;
            font-size:50px;
            margin-bottom:25%;
        }
        # button[kind="primary"].active {
        #     background-color: #FFFFFF !important; 
        #     color: black !important;
        # }
        .css-x78sv8 p{
            font-size:30px;
            
        }
        .css-183lzff {
            font-family: "Source Code Pro", monospace;
            white-space: pre;
            font-size: 30px;
            overflow-x: auto;
            color:#FFFFFF;
        }
        .stButton>button:hover, .stButton>button:focus {
            background-color: #FFFFFF !important; 
            color: black !important;
        }

        .css-183lzff {
            font-family: sans-serif;
            white-space: pre;
            font-size: 30px;
            overflow-x: auto;
            color: #FFFFFF;
            font-weight:bolder;
        }
        .css-6qob1r {
            width:100%;
            background-color: #31363F;
        }
        # .css-uf99v8 {
        #     background-color:white !important;
        # }
        .css-1nm2qww{
            background-color: #FFFFFF
        }
        # .css-k7vsyb span{
        #     margin-left:7px;
        #     font-size:34px;
        # }
        .css-1y4p8pa{
            max-width:none;
            padding-left:7rem;
            padding-top:15px;
            width:100%;
        }
        
        .css-16idsys p {
            margin-bottom: 0px;
            font-size: 30px;
            color: #FFFFFF;
            font-weight:bolder;
        }
        .css-q8sbsg p{
            font-size:35px !important;
        }
        .css-6qob1r {
            width:120%;
            # background-color:#37b610 !important;
        }
        .css-nahz7x p {
            font-size:50px !important;
            margin-bottom:20px;
        }
        .st-dk{
            font-size:150%;
        }
        .st-cd{
            font-size:150%;
        }
        [data-testid="stAppViewContainer"] > .main{
            background-image: url("https://opc-dc.gov/wp-content/uploads/2022/05/istockphoto-1247794854-612x612-1.jpg");
            background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
            background-position: center;  
            background-repeat: no-repeat;
        }

    </style>
"""
original_title = '<p style="font-family: serif; color:white; font-size: 36px;margin-top:-30px;">Dashboard </p>'

highlight_button_script = """
<script>
    const buttons = document.querySelectorAll('button[kind="primary"]');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            buttons.forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
</script>
"""

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://opc-dc.gov/wp-content/uploads/2022/05/istockphoto-1247794854-612x612-1.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
# """


# Main Streamlit app
def main():
    st.markdown(background_image, unsafe_allow_html=True)
    st.markdown(button_styles, unsafe_allow_html=True)
    # st.markdown(highlight_button_script, unsafe_allow_html=True)

    # Buttons with text in sidebar
    with st.sidebar:
        st.markdown(original_title, unsafe_allow_html=True)
        # st.write("Logged in:", st.session_state.logged_in)

        if st.button("Upload image", key="button1", type="primary"):
            # Redirect to the home page
            st.experimental_set_query_params(page="home")

        if st.button("Power prediction", key="button2", type="primary"):
            # Redirect to the prediction page
            st.experimental_set_query_params(page="prediction")

        if st.button("Previous history", key="button4", type="primary"):
            # Redirect to the account page
            st.experimental_set_query_params(page="history")

        if st.button("Govt Schemes", key="button3", type="primary"):
            # Redirect to the government schemes page
            st.experimental_set_query_params(page="govt_schemes")

        if st.button("Login/Sign-up", key="button5", type="primary"):
            # Redirect to the account page
            st.experimental_set_query_params(page="account")

    # Retrieve the page parameter from the URL
    page = st.experimental_get_query_params().get("page", [""])[0]

    # Set the default page if the app is just starting
    if not page:
        page = "account"  # Set the default page to the account page

    # Render different components based on the selected page
    if page == "home":
        home.main()
    elif page == "account":
        account.app()
    elif page == "prediction":
        input.main()
    elif page == "history":
        history.main()
    elif page == "govt_schemes":
        govscheme.main()

    # Add more elif conditions for other pages


if __name__ == "__main__":
    main()
