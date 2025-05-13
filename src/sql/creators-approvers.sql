WITH filtered_mrs AS (
  SELECT *
  FROM read_ndjson(
    'output/*.jsonl',
    auto_detect = true,
    ignore_errors = true,
    maximum_object_size = 50000000
  )
),
qualified_authors AS (
  SELECT author.username
  FROM filtered_mrs
  GROUP BY author.username
  HAVING COUNT(*) >= 5
)
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
FROM filtered_mrs AS t
JOIN qualified_authors a ON t.author.username = a.username
, UNNEST(t.approvals.approved_by) AS approved_by(user)
