import streamlit as st
import home
import account, history

# Define CSS styles for buttons and hover effects
button_styles = """
    <style>
        .orange-button {
            background-color: orange;
            color: white;
            border: 2px solid orange;
            border-radius: 5px;
            
            margin-top:15px;
            font-size: 10px;
            cursor: pointer;
            transition: background-color 0.3s, color 0.3s;
        }
        .orange-button:hover {
            background-color: white;
            color: orange;
        }
    </style>
"""
original_title = (
    '<h1 style="font-family: serif; color:black; font-size: 36px;margin-top:-50px;">Dashboard </h1>'
)

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://media.istockphoto.com/id/1455169709/photo/solar-panels-reflect-sparkling-light-and-golden-sky-clean-energy-and-environment.webp?b=1&s=170667a&w=0&k=20&c=k27ZSV3ATE-dlMcXg6P6JNJbPeQ7SBnzesCafw6dSoA=");
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
    st.markdown(original_title, unsafe_allow_html=True)

    # Buttons with text
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("Upload Image", key="button1"):
            # Redirect to the home page
            st.experimental_set_query_params(page="home")

    with col2:
        if st.button("Power Prediction", key="button2"):
            # Redirect to the prediction page
            st.experimental_set_query_params(page="prediction")

    with col3:
        if st.button("Govt-Schemes", key="button3"):
            # Redirect to the government schemes page
            st.experimental_set_query_params(page="govt_schemes")
    with col4:
        if st.button("History", key="button4"):
            # Redirect to the account page
            st.experimental_set_query_params(page="history")

    with col5:
        if st.button("Login/Sign-up", key="button5"):
            # Redirect to the account page
            st.experimental_set_query_params(page="account")

    # Retrieve the page parameter from the URL
    page = st.experimental_get_query_params().get("page", [""])[0]

    # Render different components based on the selected page
    if page == "home":
        home.main()
    elif page == "account":
        account.app()
    elif page == "history":
        history.main()
    # Add more elif conditions for other pages


if __name__ == "__main__":
    main()
