import duckdb
import logging
from pathlib import Path

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUERIES = [
    {
        "sql_path": Path("src/sql/creators-approvers.sql"),
        "output_path": Path("result/creators_approvers.csv")
    },
    {
        "sql_path": Path("src/sql/unordered-user-pairs.sql"),
        "output_path": Path("result/unordered_user_pairs.csv")
    }
]

def run_query(sql_path: Path, output_path: Path):
    try:
        query = sql_path.read_text(encoding="utf-8")
        df = duckdb.query(query).to_df()
        df.to_csv(output_path, index=False, quoting=1)
        logger.info(f"✅ Query from {sql_path.name} successful → Saved to {output_path}")
    except Exception as e:
        logger.warning(f"⚠️ DuckDB query failed for {sql_path.name}: {e}")

if __name__ == "__main__":
    for q in QUERIES:
        run_query(q["sql_path"], q["output_path"])