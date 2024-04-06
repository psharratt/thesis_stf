SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'augur_data'
ORDER BY table_name;
