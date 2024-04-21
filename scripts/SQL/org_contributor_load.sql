SELECT
    DATE_TRUNC('month', CAST(cmt_author_date AS TIMESTAMP)) AS commit_month,
    COUNT(DISTINCT cmt_author_name) AS num_contributors,
    COUNT(*) AS total_commits
FROM
    augur_data.commits
WHERE 
    repo_id IN (
        SELECT repo_id
        FROM augur_data.repo
        WHERE repo_git LIKE '%github.com/apache/%'
    )
    AND cmt_author_date <> ''  -- Exclude empty strings
    AND cmt_author_date IS NOT NULL  -- Ensure no NULL values are present
    AND CAST(cmt_author_date AS DATE) >= '2019-01-01'
    AND CAST(cmt_author_date AS DATE) <= '2024-01-01'
GROUP BY DATE_TRUNC('month', CAST(cmt_author_date AS TIMESTAMP))
ORDER BY commit_month;

