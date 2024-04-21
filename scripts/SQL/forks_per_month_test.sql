SELECT
    DATE_TRUNC('month', data_collection_date) AS month,
    SUM(repo_info.fork_count) AS total_forks
FROM
    augur_data.repo_info
WHERE
    repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%%github.com/{org_name}/%%')
GROUP BY
    month
ORDER BY
    month;
