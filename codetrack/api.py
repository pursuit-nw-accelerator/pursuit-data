from dotenv import load_dotenv
from typing import Dict, List
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


def get_user_by_id(user_id: int) -> Dict:
    """
    Fetch a user from the API
    """
    return _get(f"/users/{user_id}")


def get_weekly_scores_by_user_id(user_id: int, limit: int = 1000) -> List[Dict]:
    """
    Fetch a user's past weekly DSA points
    """
    return _get(f"/weeklyScores/{user_id}", limit=limit)


def get_weekly_commits_by_user_id(user_id: int, limit: int = 1000) -> List[Dict]:
    """
    Fetch a user's past weekly commits
    """
    return _get(f"/weeklyCommits/{user_id}", limit=limit)


def refresh_leetcode_points(user_id: int, leetcode_id: str) -> Dict:
    """
    Fetches a user's leetcode progress (number of easy, medium, hard solved)
    As a side effect, this also updates the same data in Codetrack's db
    """
    return _get(f"/leetcode/{user_id}/{leetcode_id}")
