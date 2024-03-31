SELECT
    ca.repo_id,
    ca.repo_name,
    LEFT(ca.cntrb_id::text, 15) as cntrb_id,
    TIMEZONE('utc', ca.created_at) AS created_at,
    ca.login,
    ca.action,
    ca.rank
FROM
    explorer_contributor_actions ca
WHERE
    ca.repo_id = 150824 -- testing with 'sequoia-pgp fast-forward'
    AND TIMEZONE('utc', ca.created_at) < NOW()

