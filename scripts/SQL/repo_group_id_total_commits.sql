SELECT
    SUBSTRING(r.repo_git FROM 'https://github.com/([^/]+)/.*') AS org_name,
    COUNT(c.cmt_id) AS total_commits
FROM
    augur_data.commits c
JOIN
    augur_data.repo r ON c.repo_id = r.repo_id
WHERE
    r.repo_id IN (
        SELECT repo_id
        FROM augur_data.explorer_user_repos
        WHERE login_name = 'psh1'
    )
GROUP BY
    org_name
ORDER BY
    total_commits DESC;
