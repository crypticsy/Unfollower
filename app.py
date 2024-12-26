# ----------------------------------------------- Relevant Librarires -----------------------------------------------

import streamlit as st
import zipfile

from bs4 import BeautifulSoup as bs


st.set_page_config(
    page_title="Unfollower",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

divider_color = "red"

# Steps inside a toggle
with st.expander("How to Download Instagram Follower and Following Data From Meta", icon="🤔"):
    st.divider()
    st.write("Follow the steps below to download your Instagram follower and following data from Meta.")
    
    steps = [
        "Log in to your Instagram account on the app or [website](https://www.instagram.com/).",
        "Go to your profile and tap the **Menu** (three horizontal lines) in the top-right corner.",
        "Select **Settings and Privacy**, then scroll down and click **Meta Account Center**.",
        "In the Account Center, find the **Privacy** section and select **Your Information and Permissions**.",
        "Click on **Download Your Information**.",
        "Choose the Instagram account, check **Followers and Following Data**, and select your preferred format as HTML.",
        "Click **Request a Download**. Meta will process your request and send a link to your email.",
        "Check your email for a link from Meta, and log in to your account to verify and download the file.",
        "Upload the downloaded ZIP file to view your data."
    ]

    for i, step in enumerate(steps, start=1):
        st.markdown(f"**Step {i}:** {step}")


st.markdown("<br/><br/>", unsafe_allow_html=True)
st.subheader("Upload Your Meta Data", divider=divider_color)

# File uploader
uploaded_file = st.file_uploader("", type=["zip"])

if uploaded_file:
    # Notify the user
    st.info("Processing the uploaded ZIP file...")
    
    followers = ""
    following = ""

    # Open the ZIP file in memory
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:    
        for file_name in zip_ref.namelist():
            # ensure the file is an HTML file
            if not file_name.endswith(".html"):
                continue
            
            if "followers" in file_name.split("/")[-1]:
                with zip_ref.open(file_name) as file:
                    followers = bs(file.read(), "html.parser")
                    
            elif "following" in file_name.split("/")[-1]:
                with zip_ref.open(file_name) as file:
                    following = bs(file.read(), "html.parser")
    
    if followers and following:
        st.success("Data successfully extracted!")
        
        st.markdown("<br/><br/>", unsafe_allow_html=True)
        st.subheader("Following that don't follow you back", divider=divider_color)
        followers_list = [follower.text for follower in followers.find_all("a", {"target": "_blank"})] 
        following_list = [following.text for following in following.find_all("a", {"target": "_blank"})]
        
        unfollowers = [following for following in following_list if following not in followers_list]
        
        for unfollower in unfollowers:
            st.markdown(f"👻 [{unfollower}](https://www.instagram.com/{unfollower})")


