# ----------------------------------------------- Relevant Librarires -----------------------------------------------

import json
import zipfile
import requests
import streamlit as st

from bs4 import BeautifulSoup as bs


st.set_page_config(
    page_title="Unfollower",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .block-container {
                    padding-top: 3rem;
                    padding-bottom: 3rem;
                    padding-left: 6vw;
                    padding-right: 6vw;
                }
        </style>
        """, unsafe_allow_html=True)

divider_color = "red"

# ----------------------------------------------- Main Page -----------------------------------------------

# Custom logos for the tabs
instagram_logo = "![Instagram Logo](https://cdn-icons-png.flaticon.com/512/1384/1384063.png)"
github_logo = "![GitHub Logo](https://cdn.worldvectorlogo.com/logos/github-icon-2.svg)"

st.subheader("Unfollower", divider = divider_color)
st.markdown("""
<p style="font-size: 13px; font-weight: 400;">
    A simple tool to help you identify the people on platforms who don't follow you back ! <br/>
    It is designed to help you manage your following list, 
    clearing out the accounts that don’t reciprocate your follow and letting you focus on people who genuinely care about your content. 💖
</p>
""", unsafe_allow_html=True)


st.markdown("<p style='margin-bottom:2.5px;' > 🚀 &nbsp; Features</p>", unsafe_allow_html=True)
st.markdown("""
<ul style="font-size: 13px; font-weight: 400;">
    <li>Privacy first : All processing happens locally—your data is safe!</li>
    <li>Interactive and user-friendly : See your results with a clean and intuitive interface.</li>
</ul>
""", unsafe_allow_html=True)




st.markdown("<br/>", unsafe_allow_html=True)

# Tabs with custom logos
instagram_tab, github_tab = st.tabs([
    f"{instagram_logo} &nbsp; **Instagram** &nbsp; &nbsp; ",
    f"{github_logo} &nbsp; **GitHub** &nbsp; &nbsp; "
])



# ----------------------------------------------- Instagram Tab -----------------------------------------------

with instagram_tab:
    # Steps inside a toggle
    with st.expander("&nbsp; &nbsp; How to Download Instagram Follower and Following Data From Meta", icon="📥"):
        st.divider()
        st.write("Follow the steps below to download your Instagram follower and following data from Meta.")
        
        steps = [
            "Log in to your Instagram account on the [Instagram website](https://www.instagram.com/) or the mobile app.",
            "Go to your profile and tap the **Menu** icon (three lines) in the top-right corner.",
            "Select **Settings and Privacy** and scroll down to click **Meta Account Center**.",
            "In the Account Center, go to **Privacy** and click **Your Information and Permissions**.",
            "Choose **Download Your Information**, then select **Some of your information**.",
            "Scroll down, check **Followers and Following**, and click **Next**.",
            "Select **Download to device**, choose **All time** for the date range.",
            "Click **Request a Download**. Wait for an email from Meta with your download link.",
            "Open the email, click the link, and log in to confirm your request.",
            "Download the ZIP file, and upload it to this webpage."
        ]

        for i, step in enumerate(steps, start=1):
            st.markdown(f"&nbsp; &nbsp; &nbsp; **Step {i}:** {step}")

    st.markdown("<br/>", unsafe_allow_html=True)

    # Data format
    save_type = st.radio("Data Format", ["HTML", "JSON"], index=0, horizontal=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader("Upload your zip file here", type=["zip"])

    if uploaded_file:
        with st.spinner("Processing the uploaded ZIP file..."):
            instagram_followers = ""
            instagram_following = ""
            unfollowers_instagram = []

            # Open the ZIP file in memory
            with zipfile.ZipFile(uploaded_file, "r") as zip_ref:    
                for file_name in zip_ref.namelist():            
                    if save_type == "HTML" and file_name.endswith(".html"):
                        if "followers_1.html" in file_name.split("/")[-1]:
                            with zip_ref.open(file_name) as file:
                                instagram_followers = bs(file.read(), "html.parser")
                            
                        elif "following.html" in file_name.split("/")[-1]:
                            with zip_ref.open(file_name) as file:
                                instagram_following = bs(file.read(), "html.parser")
                    
                    elif save_type == "JSON" and file_name.endswith(".json"):
                        if "followers_1.json" in file_name.split("/")[-1]:
                            with zip_ref.open(file_name) as file:
                                instagram_followers = json.load(file)
                        
                        elif "following.json" in file_name.split("/")[-1]:
                            with zip_ref.open(file_name) as file:
                                instagram_following = json.load(file)

        if instagram_followers and instagram_following and save_type == "HTML":
            st.success("Data successfully extracted!")
            
            instagram_followers_list = [follower.text for follower in instagram_followers.find_all("a", {"target": "_blank"})] 
            instagram_following_list = [followin.text for followin in instagram_following.find_all("a", {"target": "_blank"})]
            unfollowers_instagram = [following for following in instagram_following_list if following not in instagram_followers_list]
        
        elif instagram_followers and instagram_following and save_type == "JSON":
            st.success("Data successfully extracted!")
            
            instagram_followers_list = [follower["string_list_data"][0]["value"] for follower in instagram_followers]
            instagram_following_list = [followin["string_list_data"][0]["value"] for followin in instagram_following["relationships_following"]]
            unfollowers_instagram = [following for following in instagram_following_list if following not in instagram_followers_list]
        
        else:
            st.error("Please ensure you have uploaded the correct ZIP file and selected the correct data format.")
        
        if unfollowers_instagram:
            st.markdown("<br/><br/>", unsafe_allow_html=True)
            st.subheader("Users that you follow but don't follow you back", divider=divider_color)
        
            col1, col2, col3 = st.columns(3)
            col1.metric("Users that meet the criteria", len(unfollowers_instagram))
            col2.metric("Total Followers", len(instagram_followers_list))   
            col3.metric("TotalF ollowing", len(instagram_following_list))
            
            search_term = st.text_input("Search for a specific user", "", key="search_instagram")
            st.markdown("<br/>", unsafe_allow_html=True)

            instagram_filtered_search = unfollowers_instagram
            if search_term: instagram_filtered_search = [user for user in unfollowers_instagram if search_term.lower() in user.lower()]
                
            for unfollower_insta in instagram_filtered_search:
                st.markdown(f"🗑️  &nbsp; [{unfollower_insta}](https://www.instagram.com/{unfollower_insta})")
        
        elif instagram_followers and instagram_following and not unfollowers_instagram:
            st.info("You follow everyone back! 🎉", icon="🎉")



# ----------------------------------------------- GitHub Tab -----------------------------------------------

with github_tab:
    github_username = st.text_input("Enter your GitHub username", "")
    
    if github_username:
        # Check if the username exists
        with st.spinner("Checking if the username exists..."):
            response = requests.get(f"https://api.github.com/users/{github_username}")
            if response.status_code == 404:
                st.error("&nbsp; The username does not exist. Please enter a valid GitHub username.", icon="❌")
            
            else:
                github_following_html = bs(requests.get(f"https://github.com/{github_username}?tab=following").text, "html.parser")
                github_followers_html = bs(requests.get(f"https://github.com/{github_username}?tab=followers").text, "html.parser")
                
                github_following_list = [followin.text for followin in github_following_html.find_all("a", {"class": "d-inline-block"})]
                github_follower_list = [follower.text for follower in github_followers_html.find_all("a", {"class": "d-inline-block"})]
                
                github_following = [followin.split("\n")[-2] for followin in github_following_list if followin != ""]
                github_followers = [follower.split("\n")[-2] for follower in github_follower_list if follower != ""]
                
                unfollowers_github = [followin for followin in github_following if followin not in github_followers]
                
                if unfollowers_github:
                    st.markdown("<br/><br/>", unsafe_allow_html=True)
                    st.subheader("Users that you follow but don't follow you back", divider=divider_color)
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Users that meet the criteria", len(unfollowers_github))
                    col2.metric("Total Followers", len(github_followers))
                    col3.metric("Total Following", len(github_following))
                    
                    search_github = st.text_input("Search for a specific user", "", key="search_github")
                    st.markdown("<br/>", unsafe_allow_html=True)
                    
                    filtered_github_search = unfollowers_github
                    if search_github: filtered_github_search = [user for user in unfollowers_github if search_github.lower() in user.lower()]
                    
                    for unfollower_github in filtered_github_search:
                        st.markdown(f"🗑️  &nbsp; [{unfollower_github}](https://www.github.com/{unfollower_github})")

                else:
                    st.info("You follow everyone back! 🎉", icon="🎉")