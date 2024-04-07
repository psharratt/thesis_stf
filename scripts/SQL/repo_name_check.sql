SELECT repo_id, repo_name
FROM repo
WHERE LOWER(repo_name) = LOWER('logging-log4j2');