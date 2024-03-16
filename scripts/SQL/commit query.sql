SELECT repo_id, COUNT(commit_id) AS total_commits, DATE_TRUNC('month', commit_date) AS month
FROM augur_data.commits
WHERE repo_id IN (SELECT repo_id FROM augur_data.explorer_user_repos WHERE login_name='psh1')
GROUP BY repo_id, month
ORDER BY repo_id, month;
