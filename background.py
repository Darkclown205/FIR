import streamlit as st

# Set the background image
page_bg_img = '''
<style>
body {
background-image: url("data/header-bg-home.jpg");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Streamlit app content
st.title('Online FIR System')
# Additional content
