from typing import Dict, List
from datetime import datetime
import requests
import json

URL = "https://leetcode.com/graphql"
LIMIT = 20

def timestamp_to_datestr(ts: str) -> str:
    """converts timestamp to string in YYYY-MM-DD format"""
    d = datetime.fromtimestamp(int(ts))
    return d.strftime('%Y-%m-%d')

def fetch_submissions_for_user (username: str) -> List[Dict]:
    """Fetch the last 20 problems with ACs (submissions that passed all tests)
    for a particular leetcode user. 20 is a hard limit of Leetcode's API."""
    body = {
        "query": """
        query recentAcSubmissions($username: String!, $limit: Int!) {
            recentAcSubmissionList(username: $username, limit: $limit) {
                id
                title
                titleSlug
                timestamp
            }
        } 
        """,
        "variables": { "username": username, "limit": LIMIT },
        "operationName": "recentAcSubmissions"
    }
    headers = {
        "Content-Type": "application/json"
    }
    res = requests.post(URL, json.dumps(body), headers=headers)
    if not res.ok:
        res.raise_for_status()
    
    body = res.json()
    submission_list = body['data']['recentAcSubmissionList']

    submissions = []
    for submission in submission_list:
        submissions.append({ 
            "date": timestamp_to_datestr(submission["timestamp"]),
            "url": f"https://leetcode.com/problems/{submission['titleSlug']}"
            })


    return submissions
