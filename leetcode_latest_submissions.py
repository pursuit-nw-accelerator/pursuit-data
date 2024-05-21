import json
from typing import Dict, List
import sys
from datetime import datetime
from leetcode.api import fetch_submissions_for_user


def fetch_submissions_for_all_users(students: List[Dict], verbose=False) -> List[Dict]:
    """
    For each user in the roster, fetch the latest submissions
    Returns list of lists suitable for writing to a csv
    """
    students = None
    with open("rosters/roster.json") as f:
        students = json.load(f)
    
    results = []
    for student in students:
        if student["leetcode_id"] is not None:
            if verbose:
                print(f"fetching submissions for {student['email']}...")
            
            submissions = fetch_submissions_for_user(student["leetcode_id"])
            for submission in submissions:
                results.append([student['email'], submission['date'], submission['url']])
    
    return results




def main(verbose=False):

    if len(sys.argv) != 3:
        print("Usage: python leetcode_latest_submissions [start_date] [end_date], format 'YYYY-MM-DD'")
        return False
    
    start_date = sys.argv[1]
    end_date = sys.argv[2]

    if end_date < start_date:
        print("end_date must be >= start_date")
        return False

    students = None
    with open("rosters/roster.json") as f:
        students = json.load(f)

    submissions = fetch_submissions_for_all_users(students, verbose=True)
    filename = f"{end_date}_solved_problems.csv"
    with open(filename, "w+") as f:
        f.write('email,date,url\n')
        for submission in submissions:
            email, sub_date, url = submission
            if start_date <= sub_date <= end_date:
                f.write(f"{email},{sub_date},{url}\n")

if __name__ == "__main__":
    main()
