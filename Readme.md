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

## 🔐 Environment Configuration
Set up a .env file in your project root with:
```
GITLAB_API_KEY=your_gitlab_personal_access_token
PROJECT_IDS=12345678,87654321
```
GITLAB_API_KEY: A GitLab Personal Access Token with read_api scope.
PROJECT_IDS: A comma-separated list of GitLab project IDs (not names).

## ⬇️ How to Retrieve Data
To fetch merged MRs and their approvals (incrementally):
```bash
python get_gitlab_mrs.py
```
This will:

- Fetch only new merged MRs (based on latest updated_at)
- Store output per project as .jsonl files in the `output/` directory


## 🧠 SQL Analysis Example
To extract author–reviewer pairs with full context:

```sql
SELECT 
    t.project_id,
    t.project_name,
    t.id,
    t.iid,
    t.merged_at,
    t.prepared_at,
    t.author.id AS author_id,
    t.author.username AS author_username,
    approved_by.user.user.id AS approver_id,
    approved_by.user.user.username AS approver_username
FROM read_ndjson(
    'output/*.jsonl',
    auto_detect = true,
    ignore_errors = true,
    maximum_object_size = 50000000
) AS t,
UNNEST(t.approvals.approved_by) AS approved_by(user)
```

This produces a flat, analysis-ready table with one row per approval, including:
- Merge request metadata (merged_at, prepared_at)
- Author info
- Approver info

You can use the result in Looker Studio, Pandas, or Power BI to explore review dynamics, reviewer load, and cross-team interactions.