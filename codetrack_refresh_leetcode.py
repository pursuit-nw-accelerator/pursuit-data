import json
from codetrack.api import refresh_leetcode_points


def main(verbose=False):
    """
    For each user with a codetrack id and leetcode id,
    refresh the user's leetcode progress in the codetrack db.
    This is done by making a request for leetcode progress to the
    Codetrack API, which proxies the request to leetcode.
    As a side effect, the user's scores in Codetrack's database
    are updated with the latest progress from leetcode.
    """
    students = None
    with open("rosters/roster.json") as f:
        students = json.load(f)

    for student in students:
        if student["id"] > 0 and student["leetcode_id"] is not None:
            print(f"refreshing leetcode for {student['email']}...")
            results = refresh_leetcode_points(student["id"], student["leetcode_id"])
            if verbose:
                print(student["email"], results)


if __name__ == "__main__":
    main()
