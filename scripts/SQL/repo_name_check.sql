SELECT repo_id, repo_name, repo_git
FROM augur_data.repo
WHERE LOWER(repo_name) = LOWER('curl');


SELECT repo_id, repo_name, repo_git
FROM augur_data.repo
WHERE LOWER(repo_name) = LOWER('cryptography');