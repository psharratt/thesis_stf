SELECT
    /* Assuming there's a field that can be directly associated with an organization, pseudo-code here */
    COUNT(DISTINCT cm.cmt_id) AS total_contributors
FROM
    augur_data.commits cm
JOIN
    augur_data.repo r ON cm.repo_id = r.repo_id
WHERE
    cm.repo_id IN (
        SELECT repo_id 
        FROM augur_data.explorer_user_repos
        WHERE login_name = 'psh1'
    );
/* Pseudo-code to group by an organization-identifying field */
GROUP BY
    /* Organization identifying field */
ORDER BY
    total_contribitors DESC;


-- this doesn't work yet, but is close to working. 