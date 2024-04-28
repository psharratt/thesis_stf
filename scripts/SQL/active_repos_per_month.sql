WITH MonthlyCommits AS (
    SELECT
        DATE_TRUNC('month', CAST(cmt_committer_date AS TIMESTAMP)) AS month,
        repo_id
    FROM
        augur_data.commits
    WHERE
        cmt_committer_date IS NOT NULL
        AND repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%github.com/curl/%')
        AND cmt_committer_date BETWEEN '2016-01-01' AND '2024-05-01'
)
SELECT
    month,
    COUNT(DISTINCT repo_id) AS active_repositories
FROM
    MonthlyCommits
GROUP BY
    month
ORDER BY
    month;
