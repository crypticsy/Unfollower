"""Simple clean table component using Streamlit native components."""

import streamlit as st
from typing import List, Dict
import math


def render_custom_table(data: List[Dict], table_type: str = "instagram"):
    """
    Render a clean, simple table with pagination and search.

    Args:
        data: List of dictionaries containing table data
        table_type: Type of table ("instagram" or "github")
    """
    # Search and pagination controls
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input(
            "Search",
            "",
            key=f"search_{table_type}",
            placeholder="Search usernames..."
        )
    with col2:
        items_per_page = st.selectbox(
            "Per page",
            [10, 25, 50, 100],
            index=1,
            key=f"items_{table_type}"
        )

    # Initialize session state for current page and last search
    page_key = f"current_page_{table_type}"
    search_key = f"last_search_{table_type}"

    if page_key not in st.session_state:
        st.session_state[page_key] = 1
    if search_key not in st.session_state:
        st.session_state[search_key] = ""

    # Reset to page 1 if search term changed
    if st.session_state[search_key] != search_term:
        st.session_state[page_key] = 1
        st.session_state[search_key] = search_term

    # Filter data from entire dataset
    filtered_data = data
    if search_term:
        if table_type == "instagram":
            filtered_data = [
                item for item in data
                if search_term.lower() in item['username'].lower()
            ]
        else:  # GitHub - data is just a list of strings
            filtered_data = [
                item for item in data
                if search_term.lower() in item.lower()
            ]

    # Pagination after filtering
    total_items = len(filtered_data)
    total_pages = math.ceil(total_items / items_per_page) if total_items > 0 else 1

    # Ensure current page is within bounds
    current_page = min(st.session_state[page_key], total_pages) if total_pages > 0 else 1
    st.session_state[page_key] = current_page

    # Calculate slice
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    page_data = filtered_data[start_idx:end_idx]

    # Render table using Streamlit containers
    if page_data:
        st.markdown("---")

        # Header row
        if table_type == "instagram":
            header_cols = st.columns([0.5, 2, 2, 1.5])
            header_cols[0].markdown("**No.**")
            header_cols[1].markdown("**Username**")
            header_cols[2].markdown("**You Followed On**")
            header_cols[3].markdown("**Status**")

            st.markdown("<hr style='margin: 0; margin-bottom: 30px;'>", unsafe_allow_html=True)

            # Data rows
            for idx, item in enumerate(page_data, start=start_idx + 1):
                cols = st.columns([0.5, 2, 2, 1.5])
                cols[0].text(str(idx))
                cols[1].markdown(f"[{item['username']}](https://www.instagram.com/{item['username']})")
                cols[2].text(item.get('you_followed', 'N/A'))
                cols[3].markdown(":red[Not Following Back]")

        else:  # GitHub
            header_cols = st.columns([0.5, 3, 2])
            header_cols[0].markdown("**No.**")
            header_cols[1].markdown("**Username**")
            header_cols[2].markdown("**Status**")

            st.markdown("---")

            # Data rows
            for idx, username in enumerate(page_data, start=start_idx + 1):
                cols = st.columns([0.5, 3, 2])
                cols[0].text(str(idx))
                cols[1].markdown(f"[{username}](https://www.github.com/{username})")
                cols[2].markdown(":red[Not Following Back]")

        st.markdown("---")

        # Pagination info (centered)
        st.markdown(f"<div style='text-align: center; color: #6c757d; font-size: 14px; margin: 16px 0;'>Showing {start_idx + 1}-{end_idx} of {total_items} users</div>", unsafe_allow_html=True)

        # Pagination controls
        if total_pages > 1:
            col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

            with col2:
                if st.button("◀", key=f"prev_{table_type}", disabled=(current_page == 1)):
                    st.session_state[page_key] = max(1, current_page - 1)
                    st.rerun()

            with col3:
                st.markdown(f"<div style='text-align: center; padding: 8px;'>Page {current_page} of {total_pages}</div>", unsafe_allow_html=True)

            with col4:
                if st.button("▶", key=f"next_{table_type}", disabled=(current_page == total_pages)):
                    st.session_state[page_key] = min(total_pages, current_page + 1)
                    st.rerun()
    else:
        st.info("No users found matching your search.")
