"""Main application file for Unfollower Tracker."""

import json
import zipfile
import streamlit as st
from bs4 import BeautifulSoup as bs

from src.parsers.instagram_parser import (
    parse_html_followers,
    parse_html_following,
    parse_json_followers,
    parse_json_following,
    get_unfollowers
)
from src.parsers.github_parser import fetch_github_data, get_github_unfollowers
from src.components.table import render_custom_table
from src.components.ui import (
    render_header,
    render_metrics,
    render_section_header,
    apply_global_styles
)


# Page configuration
st.set_page_config(
    page_title="Unfollower Tracker",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply global styles
apply_global_styles()

# Render header
render_header()

# Custom logos for the tabs
instagram_logo = "![Instagram](https://cdn-icons-png.flaticon.com/512/1384/1384063.png)"
github_logo = "![GitHub](https://www.svgrepo.com/show/475654/github-color.svg)"

# Tabs
instagram_tab, github_tab = st.tabs([
    f"{instagram_logo} &nbsp; **Instagram** &nbsp; &nbsp; ",
    f"{github_logo} &nbsp; **GitHub** &nbsp; &nbsp; "
])


# ----------------------------------------------- Instagram Tab -----------------------------------------------

with instagram_tab:
    # Instructions
    with st.expander("📥 How to Download Instagram Data from Meta", expanded=False):
        st.markdown("""
        ### Follow these steps to get your Instagram data:

        1. Log in to [Instagram](https://www.instagram.com/)
        2. Go to **Menu** → **Settings and Privacy** → **Meta Account Center**
        3. Navigate to **Privacy** → **Your Information and Permissions**
        4. Select **Download Your Information** → **Some of your information**
        5. Check **Followers and Following**, then click **Next**
        6. Choose **Download to device** with **All time** date range
        7. Click **Request a Download** and wait for the email
        8. Download the ZIP file and upload it below
        """)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Data format selector
    save_type = st.radio("📄 Data Format", ["HTML", "JSON"], index=0, horizontal=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader("📤 Upload your ZIP file from Meta", type=["zip"])

    if uploaded_file:
        with st.spinner("🔄 Processing your data..."):
            instagram_followers = ""
            instagram_following = ""
            unfollowers_instagram_detailed = []

            # Open the ZIP file
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

        # Parse data
        if instagram_followers and instagram_following and save_type == "HTML":
            st.success("✅ Data successfully extracted!")

            followers_data = parse_html_followers(instagram_followers)
            following_data = parse_html_following(instagram_following)
            unfollowers_instagram_detailed = get_unfollowers(followers_data, following_data)

        elif instagram_followers and instagram_following and save_type == "JSON":
            st.success("✅ Data successfully extracted!")

            followers_data = parse_json_followers(instagram_followers)
            following_data = parse_json_following(instagram_following)
            unfollowers_instagram_detailed = get_unfollowers(followers_data, following_data)

        else:
            st.error("❌ Please ensure you uploaded the correct ZIP file and selected the correct data format.")

        # Display results
        if unfollowers_instagram_detailed:
            instagram_followers_list = list(followers_data.keys()) if 'followers_data' in locals() else []
            instagram_following_list = list(following_data.keys()) if 'following_data' in locals() else []

            # Render metrics
            render_metrics(
                len(unfollowers_instagram_detailed),
                len(instagram_followers_list),
                len(instagram_following_list)
            )

            # Render section header
            render_section_header("Users Not Following You Back", "👥")

            # Render custom table
            render_custom_table(unfollowers_instagram_detailed, table_type="instagram")

        elif instagram_followers and instagram_following and not unfollowers_instagram_detailed:
            st.success("🎉 Amazing! Everyone you follow follows you back!")


# ----------------------------------------------- GitHub Tab -----------------------------------------------

with github_tab:
    st.markdown("### 🔍 Enter GitHub Username")
    github_username = st.text_input("", placeholder="Enter username...", key="github_username", label_visibility="collapsed")

    if github_username:
        with st.spinner("🔄 Fetching GitHub data..."):
            success, github_followers, github_following = fetch_github_data(github_username)

            if not success:
                st.error("❌ Username not found. Please enter a valid GitHub username.")
            else:
                unfollowers_github = get_github_unfollowers(github_followers, github_following)

                if unfollowers_github:
                    # Render metrics
                    render_metrics(
                        len(unfollowers_github),
                        len(github_followers),
                        len(github_following)
                    )

                    # Render section header
                    render_section_header("Users Not Following You Back", "👥")

                    # Render custom table
                    render_custom_table(unfollowers_github, table_type="github")

                else:
                    st.success("🎉 Amazing! Everyone you follow follows you back!")
