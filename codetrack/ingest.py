import os
from typing import Dict, List
from codetrack.api import get_weekly_commits_by_user_id, get_weekly_scores_by_user_id
from codetrack.schema import weekly_stats_schema, weekly_stats_column_names
import pyarrow as pa
import pyarrow.parquet as pq

MAX_FETCH_LIMIT = 1000
MAX_OPEN_FILES = 1024
SLICE_SIZE = 500


def ingest_weekly_stats(roster: List[Dict], limit=1) -> None:
    """
    Ingest past stats for a roster and save to parquet dataset.
    """
    rows = fetch_weekly_stats(roster, limit=limit)
    table = to_arrow_table(rows)
    write_to_dataset(table)


def ingest_historical_stats(roster: List[Dict]) -> None:
    """
    Ingest all past stats for a roster. Use this to ingest
    initial data but not on a regular basis (it will duplicate past data)
    """
    return ingest_weekly_stats(roster, MAX_FETCH_LIMIT)


def simplify_date_str(date_str: str) -> str:
    """
    Remove hours, minutes, etc. from ISO date string,
    leaving only YYYY-MM-DD
    """
    return date_str.split("T")[0]


def get_weekly_stats_rows_for_user(student: Dict, limit: int) -> List[Dict]:
    """
    Fetches weekly stats for a user and returns table rows
    in the format: [YYYY-MM-DD, year, month, day, email,
    cohort, codetrack id, num_points, num_commits]
    """
    id = student["id"]
    email = student["email"]
    cohort = student["cohort"]

    weekly_points = get_weekly_scores_by_user_id(id, limit)
    weekly_commits = get_weekly_commits_by_user_id(id, limit)

    # collate points by date
    by_date = {}
    for week in weekly_points:
        date = simplify_date_str(week["date"])
        # set commits = 0 as default, to be overwritten next
        by_date[date] = [week["points"], 0]

    for week in weekly_commits:
        date = simplify_date_str(week["date"])
        if date in by_date:
            # overwrite commits with actual value
            by_date[date][1] = week["points"]
        else:
            # there weren't DSA points for this date, set to 0
            by_date[date] = [0, week["points"]]

    # convert dictionary to array of rows
    # each row is a dictionary representing
    # the weekly stats for a specific user and date
    rows = []
    for date in by_date:
        year, month, day = date.split("-")
        points, commits = by_date[date]
        values = [
            date,
            int(year),
            int(month),
            int(day),
            email,
            cohort,
            id,
            points,
            commits,
        ]
        rows.append(dict(zip(weekly_stats_column_names, values)))
    return rows


def fetch_weekly_stats(roster: List[Dict], limit: int = 1) -> List[Dict]:
    """
    Fetch weekly stats for a class roster from Codetrack API.
    Returns a list of row objects that can be turned into a Pyarrow table.
    """
    rows = []
    for student in roster:
        print(f"Processing {student['email']}...")
        curr_rows = get_weekly_stats_rows_for_user(student, limit)
        rows += curr_rows

    return rows


def to_arrow_table(rows: List[Dict]) -> pa.Table:
    """
    Convert a list of rows to an in-memory Pyarrow table.
    This is an optimized column-oriented table with a set schema,
    suitable to be written to big data file formats like .parquet
    """
    struct_array = pa.array(rows)  # convert rows to a pa StructArray
    table = pa.Table.from_struct_array(struct_array)  # initialize table

    # cast to the schema (this ensures that date strings are parsed as dates)
    table = table.cast(weekly_stats_schema)
    return table


def write_to_dataset(table: pa.Table) -> None:
    # find / create the path for the dataset
    dirname = os.path.dirname(os.path.realpath(__file__))
    dataset_path = os.path.join(dirname, "data")
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    # Partition the data into zero-copy slices and write one slice at a time.
    # This is a workaround to prevent a "too many open files"
    # error that happens when writing to many partitions at once.
    # I don't know if doing this makes me stupid or smart, but here it is.
    num_rows = table.shape[0]
    slices = []
    if num_rows < MAX_OPEN_FILES:
        slices = [table]
    else:
        rows_written = 0
        while rows_written < num_rows:
            length = min(SLICE_SIZE, num_rows - rows_written)
            slices.append(table.slice(offset=rows_written, length=length))
            rows_written += length

    # write the data
    print(f"Writing the data in {len(slices)} slice(s)...")
    for i in range(len(slices)):
        print(f"\tWriting slice {i}...")
        pq.write_to_dataset(
            slices[i],
            root_path=dataset_path,
            partition_cols=["year", "month", "cohort"],
            max_rows_per_group=100,
        )
