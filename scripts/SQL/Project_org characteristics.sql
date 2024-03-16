SELECT repo_id, created_at AS project_start_date, primary_language, license
FROM augur_data.repo
WHERE repo_id IN (SELECT repo_id FROM augur_data.explorer_user_repos WHERE login_name='psh1');


DRAFT - THIS DOESN'T WORK YET