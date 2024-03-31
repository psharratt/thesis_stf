SELECT repo_id, COUNT(pull_request_id) AS total_pull_requests, DATE_TRUNC('month', created_at) AS month
FROM augur_data.pull_requests
WHERE repo_id IN (SELECT repo_id FROM augur_data.explorer_user_repos WHERE login_name='psh1')
GROUP BY repo_id, month
ORDER BY repo_id, month;

-- DRAFT - THIS DOESN'T WORK YET