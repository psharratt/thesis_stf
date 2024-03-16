SELECT
    repo_id, release_name
FROM
    augur_data.releases
-- WHERE 
--    repo_id = 150824 -- sequoia pgp as test
--    AND release_published_at > '2021-01-01'
--    AND release_published_at <= '2021-12-31'
-- ORDER BY release_name;

-- DRAFT - THIS DOESN'T WORK YET
-- think i need to specify the table as in the case of the group repo request
-- OK this is locked for some reason, even when I add repo_id
-- ah it may mean that there are no releases for sequioa
-- nope, there should be a release 'Merge Pull Requests by Fast Forwarding the Target Branch'


-- Below is code for seeing all of the releases for the groups that I've created on Augur

SELECT 
    repo.repo_id, 
    releases.release_id, 
    releases.release_name, 
    releases.release_created_at,
	releases.release_published_at,
	releases.release_updated_at
FROM 
    augur_data.releases
INNER JOIN 
    augur_data.repo ON augur_data.releases.repo_id = augur_data.repo.repo_id
INNER JOIN 
    augur_data.explorer_user_repos ON augur_data.repo.repo_id = augur_data.explorer_user_repos.repo_id
WHERE 
    augur_data.explorer_user_repos.login_name = 'psh1'
ORDER BY 
    augur_data.releases.repo_id, 
    augur_data.releases.release_published_at;

-- OK but some missing data here. 

