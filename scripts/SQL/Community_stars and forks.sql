SELECT repo_id, stars_count, forks_count
FROM augur_data.repo
WHERE repo_id IN (SELECT repo_id FROM augur_data.explorer_user_repos WHERE login_name='psh1');
