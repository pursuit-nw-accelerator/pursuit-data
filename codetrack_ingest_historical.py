import json
from codetrack.ingest import ingest_historical_stats

if __name__ == "__main__":
    students = None
    with open("rosters/roster.json") as f:
        students = json.load(f)

    ingest_historical_stats(students)
