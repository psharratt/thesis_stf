SELECT
    DATE_TRUNC('month', rl_analysis_date) AS month,
    COUNT(DISTINCT programming_language) AS distinct_languages
FROM
    augur_data.repo_labor
WHERE
    repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%%github.com/curl/%%')
    AND rl_analysis_date BETWEEN '2016-01-01' AND '2024-05-01'
    AND programming_language IS NOT NULL
GROUP BY
    month
ORDER BY
    month;
