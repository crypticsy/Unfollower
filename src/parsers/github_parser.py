"""GitHub data parser module."""

import requests
from bs4 import BeautifulSoup as bs
from typing import List, Tuple


def fetch_github_page(username: str, tab: str, page: int = 1) -> Tuple[List[str], bool]:
    """
    Fetch a single page of GitHub followers or following.

    Args:
        username: GitHub username
        tab: Either "followers" or "following"
        page: Page number to fetch

    Returns:
        Tuple of (users_list, has_next_page)
    """
    # Use GitHub's exact URL format: ?page=X&tab=Y
    if page == 1:
        url = f"https://github.com/{username}?tab={tab}"
    else:
        url = f"https://github.com/{username}?page={page}&tab={tab}"

    response = requests.get(url)
    html = bs(response.text, "html.parser")

    # Parse users
    user_elements = html.find_all("a", {"class": "d-inline-block"})
    users = [
        user.text.split("\n")[-2]
        for user in user_elements
        if user.text.strip() != ""
    ]

    # Check if there's a next page by looking for the next button
    pagination = html.find("div", {"class": "pagination"})
    has_next = False
    if pagination:
        next_link = pagination.find("a", string="Next")
        has_next = next_link is not None

    return users, has_next


def fetch_all_github_users(username: str, tab: str) -> List[str]:
    """
    Fetch all followers or following for a user (handles pagination).

    Args:
        username: GitHub username
        tab: Either "followers" or "following"

    Returns:
        Complete list of users
    """
    all_users = []
    page = 1
    has_next = True

    while has_next:
        users, has_next = fetch_github_page(username, tab, page)
        all_users.extend(users)
        page += 1

        # Safety limit to prevent infinite loops
        if page > 100:
            break

    return all_users


def fetch_github_data(username: str) -> Tuple[bool, List[str], List[str]]:
    """
    Fetch GitHub followers and following for a user.

    Args:
        username: GitHub username

    Returns:
        Tuple of (success, followers_list, following_list)
    """
    # Check if the username exists
    response = requests.get(f"https://api.github.com/users/{username}")
    if response.status_code == 404:
        return False, [], []

    # Fetch all followers and following (with pagination)
    github_followers = fetch_all_github_users(username, "followers")
    github_following = fetch_all_github_users(username, "following")

    return True, github_followers, github_following


def get_github_unfollowers(followers: List[str], following: List[str]) -> List[str]:
    """
    Calculate GitHub unfollowers.

    Args:
        followers: List of GitHub followers
        following: List of GitHub following

    Returns:
        List of usernames who don't follow back
    """
    return [followin for followin in following if followin not in followers]
