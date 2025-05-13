import duckdb
import logging
from pathlib import Path

# Configuration
SQL_PATH = Path("src/sql/creators-approvers.sql")
OUTPUT_PATH = Path("result/result.csv")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_query(sql_path=SQL_PATH, output_path=OUTPUT_PATH):
    try:
        query = sql_path.read_text(encoding="utf-8")
        df = duckdb.query(query).to_df()
        df.to_csv(output_path, index=False, quoting=1)  # quoting=1 = csv.QUOTE_ALL
        logger.info(f"Query successful. Output saved to {output_path}")
        print(df)
    except Exception as e:
        logger.warning(f"DuckDB query failed: {e}")

if __name__ == "__main__":
    run_query()