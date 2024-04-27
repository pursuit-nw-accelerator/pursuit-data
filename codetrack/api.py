from dotenv import load_dotenv
import requests
import os

load_dotenv()

API_URL = os.getenv("API_URL")


def _get(path: str, **kwargs: dict) -> any:
    """
    Wrapper for get requests
    """
    res = requests.get(f"{API_URL}{path}", params=kwargs)
    # throws an error for non-200 response
    if not res.ok:
        res.raise_for_status()

    return res.json()


def get_user_by_id(user_id):
    """
    Fetch a user from the API
    """
    return _get(f"/users/{user_id}")


def get_weekly_scores_by_user_id(user_id, limit=1000):
    """
    Fetch a user's past weekly DSA points
    """
    return _get(f"/weeklyScores/{user_id}", limit=limit)


def get_weekly_commits_by_user_id(user_id, limit=1000):
    """
    Fetch a user's past weekly commits
    """
    return _get(f"/weeklyCommits/{user_id}", limit=limit)
