"""UI components for the app."""

import streamlit as st


def render_header():
    """Render clean app header."""
    st.markdown("""
        <style>
        .simple-header {
            padding: 20px 0;
            margin-bottom: 30px;
            border-bottom: 2px solid #e0e0e0;
        }
        .simple-title {
            font-size: 32px;
            font-weight: 600;
            color: #2c3e50;
            margin: 0;
        }
        .simple-subtitle {
            font-size: 16px;
            color: #7f8c8d;
            margin-top: 8px;
        }
        </style>
        <div class="simple-header">
            <h1 class="simple-title">Unfollower Tracker</h1>
            <p class="simple-subtitle">
                Find out who's not following you back
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_metrics(unfollowers_count: int, followers_count: int, following_count: int):
    """
    Render simple metrics cards.

    Args:
        unfollowers_count: Number of unfollowers
        followers_count: Total followers
        following_count: Total following
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Unfollowers", f"{unfollowers_count:,}")

    with col2:
        st.metric("Total Followers", f"{followers_count:,}")

    with col3:
        st.metric("Total Following", f"{following_count:,}")


def render_section_header(title: str, icon: str = "📊"):
    """
    Render a simple section header.

    Args:
        title: Section title
        icon: Icon for the section
    """
    st.subheader(f"{icon} {title}")


def apply_global_styles():
    """Apply minimal global CSS styles to the app."""
    st.markdown("""
        <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
