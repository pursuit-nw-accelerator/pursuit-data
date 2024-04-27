import json
from codetrack.ingest import ingest_weekly_stats

if __name__ == "__main__":
    students = None
    with open("rosters/roster.json") as f:
        students = json.load(f)

    ingest_weekly_stats(students)
