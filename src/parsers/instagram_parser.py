"""Instagram data parser module."""

from datetime import datetime
from bs4 import BeautifulSoup as bs
from typing import Dict, List


def parse_html_followers(instagram_followers) -> Dict[str, str]:
    """
    Extract followers with dates from HTML.

    Args:
        instagram_followers: BeautifulSoup object of followers HTML

    Returns:
        Dictionary mapping username to follow date
    """
    followers_data = {}
    for entry in instagram_followers.find_all("div", {"class": "pam _3-95 _2ph- _a6-g uiBoxWhite noborder"}):
        link = entry.find("a", {"target": "_blank"})
        divs = entry.find_all("div")
        if link and len(divs) >= 4:
            username = link.text.strip()
            date_text = divs[3].text.strip() if divs[3].text.strip() else "N/A"
            followers_data[username] = date_text
    return followers_data


def parse_html_following(instagram_following) -> Dict[str, str]:
    """
    Extract following with dates from HTML.

    Args:
        instagram_following: BeautifulSoup object of following HTML

    Returns:
        Dictionary mapping username to follow date
    """
    following_data = {}
    for entry in instagram_following.find_all("div", {"class": "pam _3-95 _2ph- _a6-g uiBoxWhite noborder"}):
        h2 = entry.find("h2", {"class": "_3-95 _2pim _a6-h _a6-i"})
        divs = entry.find_all("div")
        if h2 and len(divs) >= 4:
            username = h2.text.strip()
            date_text = divs[3].text.strip() if divs[3].text.strip() else "N/A"
            following_data[username] = date_text
    return following_data


def parse_json_followers(instagram_followers) -> Dict[str, str]:
    """
    Extract followers with timestamps from JSON.

    Args:
        instagram_followers: List of follower JSON objects

    Returns:
        Dictionary mapping username to follow date
    """
    followers_data = {}
    for follower in instagram_followers:
        try:
            if "string_list_data" in follower and len(follower["string_list_data"]) > 0:
                username = follower["string_list_data"][0].get("value")
                if username:
                    timestamp = follower["string_list_data"][0].get("timestamp", 0)
                    date_text = datetime.fromtimestamp(timestamp).strftime("%b %d, %Y %I:%M %p") if timestamp else "N/A"
                    followers_data[username] = date_text
        except (KeyError, IndexError, TypeError):
            continue
    return followers_data


def parse_json_following(instagram_following) -> Dict[str, str]:
    """
    Extract following with timestamps from JSON.

    Args:
        instagram_following: JSON object containing relationships_following

    Returns:
        Dictionary mapping username to follow date
    """
    following_data = {}

    # Handle different JSON structures
    following_list = []
    if isinstance(instagram_following, dict):
        following_list = instagram_following.get("relationships_following", [])
    elif isinstance(instagram_following, list):
        following_list = instagram_following

    for followin in following_list:
        try:
            # Username is in the "title" field for following
            username = followin.get("title", "")

            if username and "string_list_data" in followin and len(followin["string_list_data"]) > 0:
                timestamp = followin["string_list_data"][0].get("timestamp", 0)
                date_text = datetime.fromtimestamp(timestamp).strftime("%b %d, %Y %I:%M %p") if timestamp else "N/A"
                following_data[username] = date_text
        except (KeyError, IndexError, TypeError):
            continue

    return following_data


def get_unfollowers(followers_data: Dict[str, str], following_data: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Calculate unfollowers from followers and following data.

    Args:
        followers_data: Dictionary of followers
        following_data: Dictionary of following

    Returns:
        List of unfollower dictionaries with username and dates
    """
    unfollowers_detailed = []
    for username in following_data.keys():
        if username not in followers_data:
            unfollowers_detailed.append({
                'username': username,
                'you_followed': following_data.get(username, 'N/A'),
                'they_followed': 'Never'
            })
    return unfollowers_detailed
