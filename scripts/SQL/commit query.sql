SELECT 
    repo_id, 
    COUNT(cmt_id) AS total_commits, 
    DATE_TRUNC('month', cmt_committer_date::timestamp) AS month
FROM 
    augur_data.commits
WHERE 
    repo_id IN (
        SELECT repo_id 
        FROM augur_data.explorer_user_repos 
        WHERE login_name='psh1'
    )
GROUP BY 
    repo_id, 
    DATE_TRUNC('month', cmt_committer_date::timestamp)
ORDER BY 
    repo_id, month;


-- Takes a while to run.