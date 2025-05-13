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
),
author_approver_pairs AS (
  SELECT 
    t.author.username AS author,
    approved_by.user.user.username AS approver
  FROM filtered_mrs t
  JOIN qualified_authors a ON t.author.username = a.username
  , UNNEST(t.approvals.approved_by) AS approved_by(user)
  WHERE approved_by.user.user.username IS NOT NULL
),
normalized_pairs AS (
  SELECT 
    CASE WHEN author < approver THEN author ELSE approver END AS user_a,
    CASE WHEN author < approver THEN approver ELSE author END AS user_b
  FROM author_approver_pairs
)
SELECT 
  user_a,
  user_b,
  COUNT(*) AS interactions
FROM normalized_pairs
GROUP BY user_a, user_b
having interactions>=5
ORDER BY interactions DESC
