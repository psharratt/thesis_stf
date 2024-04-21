SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'augur_data' 
  AND table_name   = 'repo_test_coverage'; 