import pyarrow as pa

weekly_stats_column_names = [
    "date",
    "year",
    "month",
    "day",
    "email",
    "cohort",
    "id",
    "points",
    "commits",
]


weekly_stats_column_types = [
    pa.date32(),
    pa.int64(),
    pa.int64(),
    pa.int32(),
    pa.string(),
    pa.string(),
    pa.int64(),
    pa.int64(),
    pa.int64(),
]

weekly_stats_schema = pa.schema(
    sorted(zip(weekly_stats_column_names, weekly_stats_column_types))
)
