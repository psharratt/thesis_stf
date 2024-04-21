SELECT
    DATE_TRUNC('month', pr_created_at) AS month,
    SUM(CASE WHEN pr_closed_at IS NULL THEN 1 ELSE 0 END) AS open_pull_requests,
    SUM(CASE WHEN pr_closed_at IS NOT NULL THEN 1 ELSE 0 END) AS closed_pull_requests
FROM
    augur_data.pull_requests
WHERE
    repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%github.com/{org_name}/%')
GROUP BY
    month
ORDER BY
    month;

SELECT
    DATE_TRUNC('month', pr_created_at) AS month,
    COUNT(DISTINCT pr_html_url) AS unique_pull_requests
FROM
    augur_data.pull_requests
WHERE
    pr_html_url LIKE '%github.com/curl/%'  -- Directly using pr_html_url to filter by organization
GROUP BY
    month
ORDER BY
    month;


SELECT
    DATE_TRUNC('month', pr_created_at) AS month,
    COUNT(DISTINCT pr_html_url) AS unique_pull_requests
FROM
    augur_data.pull_requests
WHERE
    pr_html_url LIKE '%github.com/curl/%'
    AND pr_created_at BETWEEN '2016-01-01' AND '2024-05-01'
GROUP BY
    month
ORDER BY
    month;


