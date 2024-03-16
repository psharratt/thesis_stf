SELECT repo_id, AVG(EXTRACT(epoch FROM (closed_at - created_at))/3600) AS avg_resolution_time_hours
FROM augur_data.issues
WHERE repo_id IN (SELECT repo_id FROM augur_data.explorer_user_repos WHERE login_name='psh1') AND state = 'closed'
GROUP BY repo_id;

DRAFT - THIS DOESN'T WORK YET