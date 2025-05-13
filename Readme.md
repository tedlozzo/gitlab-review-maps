# GitLab Merge Request Reviewer Analysis

This project retrieves **merged GitLab Merge Requests** along with their **approvals**, and enables data-driven analysis of **reviewer-author relationships** using DuckDB and pandas.

---

## 🔍 Purpose

This tool helps answer key engineering insights, such as:

- Who reviews whom the most (or the least)?
- Are there anomalies or review silos in the team?
- How long do MRs take to be merged?
- What are the reviewer dynamics across projects?

It fetches the data incrementally and stores it in newline-delimited JSON (`.jsonl`) for downstream analysis.

---

## ⚙️ Setup & Dependencies

Install dependencies with:

```bash
pip install -r requirements.txt
```

Required packages:
```
dotenv==0.9.9
requests==2.32.3
duckdb==1.2.2
pandas==2.2.3
```

🔐 Environment Configuration
Set up a .env file in your project root with:

env
Copy
Edit
GITLAB_API_KEY=your_gitlab_personal_access_token
PROJECT_IDS=12345678,87654321
GITLAB_API_KEY: A GitLab Personal Access Token with read_api scope.

PROJECT_IDS: A comma-separated list of GitLab project IDs (not names).

⬇️ How to Retrieve Data
To fetch merged MRs and their approvals (incrementally):

bash
Copy
Edit
python get_gitlab_mrs.py
This will:

Fetch only new merged MRs (based on latest updated_at)

Store output per project as .jsonl files in the output/ directory

Include approval data for each MR

📊 How to Analyze and Dump Results
To run SQL analysis and output results as a CSV:

bash
Copy
Edit
python run_sql_query.py
This will:

Load a SQL file (e.g. src/sql/creators-approvers.sql)

Query .jsonl files using DuckDB

Export the result to result/result.csv

You can then use result.csv in:

Looker Studio

Excel

Dashboards

Jupyter Notebooks

📁 Project Structure
text
Copy
Edit
.
├── get_gitlab_mrs.py           # Main data retriever
├── run_sql_query.py            # Run SQL analysis and export
├── utils.py                    # Helper functions (API, DuckDB)
├── output/                     # Raw .jsonl data per project
├── result/                     # Processed .csv outputs
├── src/sql/creators-approvers.sql  # Your analysis SQL
├── requirements.txt
├── .env.example
└── README.md
🧪 Example Questions to Explore
Who dominates review activity for specific authors?

Are some authors only reviewed by a single person?

How does review load distribute across the team?

These can be answered with queries in creators-approvers.sql and visualized via Looker Studio or Python.

