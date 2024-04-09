import streamlit as st
import home
# Define CSS styles for buttons and hover effects
button_styles = """
    <style>
        .orange-button {
            background-color: orange;
            color: white;
            border: 2px solid orange;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 36px;
            cursor: pointer;
            transition: background-color 0.3s, color 0.3s;
        }
        .orange-button:hover {
            background-color: white;
            color: orange;
        }
    </style>
"""
original_title = '<h1 style="font-family: serif; color:black; font-size: 36px;">Dashboard </h1>'

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
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Upload Pic", key="button1"):
           home.main()
    with col2:
        if st.button("Prediciton", key="button2"):
            st.write("Button 2 clicked!")
    with col3:
        if st.button("Govt-Schemes", key="button3"):
            st.write("Button 3 clicked!")

if __name__ == "__main__":
    main()
