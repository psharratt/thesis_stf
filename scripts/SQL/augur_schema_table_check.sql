SELECT * 
FROM information_schema.tables 
WHERE table_schema = 'augur_data' 
AND table_name = 'explorer_contributor_actions';

-- or for views
SELECT * 
FROM information_schema.views 
WHERE table_schema = 'augur_data' 
AND table_name = 'explorer_contributor_actions';

-- testing schema location with 'explorer_contributor_actions'


