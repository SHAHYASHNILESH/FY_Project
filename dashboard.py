import streamlit as st
import home, input
import account, history

# Define CSS styles for buttons and hover effects
button_styles = """
    <style>
        .orange-button {
            background-color: green;
            color: white;
            border: 2px solid green;
            border-radius: 5px;
            margin-top:15px;
            font-size: 10px;
            cursor: pointer;
            transition: background-color 0.3s, color 0.3s;
        }
        .orange-button:hover {
            background-color: white;
            color: green;
        }
        button[kind="primary"] {
            background-color: black;
            color:white;
            width:250px;
            height:80px;
            margin:10px;
            border: 3px solid green;
            border-radius: 15px;
        }
    </style>
"""
original_title = '<h1 style="font-family: serif; color:white; font-size: 36px;margin:15px;">Dashboard </h1>'

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://opc-dc.gov/wp-content/uploads/2022/05/istockphoto-1247794854-612x612-1.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""


# Main Streamlit app
def main():
    st.markdown(background_image, unsafe_allow_html=True)
    st.markdown(button_styles, unsafe_allow_html=True)
    
    # Buttons with text in sidebar
    with st.sidebar:
        st.markdown(original_title, unsafe_allow_html=True)
        if st.button("Upload Image", key="button1", type="primary"):
            # Redirect to the home page
            st.experimental_set_query_params(page="home")

        if st.button("Power Prediction", key="button2", type="primary"):
            # Redirect to the prediction page
            st.experimental_set_query_params(page="prediction")

        if st.button("Govt-Schemes", key="button3", type="primary"):
            # Redirect to the government schemes page
            st.experimental_set_query_params(page="govt_schemes")

        if st.button("History", key="button4", type="primary"):
            # Redirect to the account page
            st.experimental_set_query_params(page="history")

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
    # Add more elif conditions for other pages


if __name__ == "__main__":
    main()
