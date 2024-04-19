SELECT repo_id
FROM augur_data.repo
WHERE repo_git LIKE '%github.com/fortran-lang/%';


-- this works for getting the repo_ids for all Fortran lang repos