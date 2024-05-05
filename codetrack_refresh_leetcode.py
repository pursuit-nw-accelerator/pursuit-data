import json
from codetrack.api import refresh_leetcode_points


def main(verbose=False):
    """
    Get the leetcode id for each user
    """
    students = None
    with open("rosters/roster.json") as f:
        students = json.load(f)

    for student in students:
        if student["id"] > 0 and student["leetcode_id"] is not None:
            results = refresh_leetcode_points(student["id"], student["leetcode_id"])
            if verbose:
                print(student["email"], results)


if __name__ == "__main__":
    main()
