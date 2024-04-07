-- this query finds the repo belonging to GStreamer with the highest number 
-- of commits in the past four years.

SELECT repo_id, COUNT(cmt_id) AS total_commits
FROM augur_data.commits
WHERE repo_id IN (191527, 191537, 191528, 191533, 191541, 191545, 191538, 191546, 191548, 191544, 191532, 191530, 191529, 191531, 191536, 191535, 191534, 191540, 191547, 191542)
  AND CAST(cmt_committer_date AS TIMESTAMP) >= CURRENT_DATE - INTERVAL '4 years'
GROUP BY repo_id
ORDER BY total_commits DESC
LIMIT 3;

