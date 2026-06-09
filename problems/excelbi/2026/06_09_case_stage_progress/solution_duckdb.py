from pathlib import Path

import duckdb

from utils import show

base_path = Path(__file__).parent

data_file = base_path / "data" / "cases.csv"
sql_file = base_path / "solution.sql"

with open(sql_file, "r", encoding="utf-8") as f:
    query = f.read()

con = duckdb.connect()

con.execute(
    f"""
    CREATE OR REPLACE VIEW cases AS
    SELECT *
    FROM read_csv_auto('{data_file.as_posix()}');
    """
)

result = con.execute(query).df()

show(result, "Case Summary")
