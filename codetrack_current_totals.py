import json
from datetime import datetime
from typing import Dict, List
from codetrack.api import get_user_by_id

POINT_FIELDS = ["free_code_camp_points", "honor", "leetcode_points"]


def codetrack_current_totals(students: List[Dict], verbose=False) -> None:
    results = []
    for student in students:
        id = student["id"]  # codetrack id
        if id > 0:  # skip students who don't have a codetrack account
            if verbose:
                print(f"getting current score for {student['email']}...")
            profile = get_user_by_id(id)
            total_score = 0
            for field in POINT_FIELDS:
                total_score += profile[field]
            results.append(f"{student['email']},{total_score}\n")

    return results


def main():
    """
    This is a quicker way to get the current total scores for your class
    without having to ingest data, etc.
    You still need a roster.json file with email and codetrack id for
    each of your learners.
    """
    students = None
    with open("rosters/roster.json") as f:
        students = json.load(f)

    results = codetrack_current_totals(students, verbose=True)

    with open(f"{datetime.today().strftime('%Y-%m-%d')}_totals.csv", "w+") as f2:
        f2.write("email,score\n")
        for result in results:
            f2.write(result)


if __name__ == "__main__":
    main()
