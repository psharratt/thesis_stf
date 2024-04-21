SELECT
    DATE_TRUNC('month', data_collection_date) AS month,
    SUM(stars_count) AS total_stars
FROM
    augur_data.repo_info
WHERE
    repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%%github.com/fortran-lang/%%')
GROUP BY
    month
ORDER BY
    month;
