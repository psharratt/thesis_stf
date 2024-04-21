SELECT
    r.repo_id,
    r.repo_name,
    i.issue_id AS issue,
    i.gh_issue_number AS issue_number,
    i.gh_issue_id AS gh_issue,
    LEFT(i.reporter_id::TEXT, 15) AS reporter_id,
    LEFT(i.cntrb_id::TEXT, 15) AS issue_closer,
    i.created_at,
    i.closed_at
FROM
    augur_data.repo r,
    augur_data.issues i
WHERE
    r.repo_id = i.repo_id AND
    r.repo_id IN (193661)  -- Use just the number for a single ID
    AND i.pull_request_id IS NULL
    AND i.created_at < NOW()
    AND (i.closed_at < NOW() OR i.closed_at IS NULL)
ORDER BY
    i.created_at;
