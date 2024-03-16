SELECT repo_id, COUNT(DISTINCT author_id) AS unique_contributors
FROM augur_data.commits
WHERE repo_id IN (SELECT repo_id FROM augur_data.explorer_user_repos WHERE login_name='psh1')
GROUP BY repo_id;


DRAFT - THIS DOESN'T WORK YET