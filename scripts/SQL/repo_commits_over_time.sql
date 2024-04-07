SELECT
  repo_id,
  EXTRACT(YEAR FROM CAST(cmt_author_date AS DATE)) AS year,
  EXTRACT(MONTH FROM CAST(cmt_author_date AS DATE)) AS month,
  COUNT(*) AS total_commits
FROM
  augur_data.commits
WHERE
  repo_id IN (150978, 150822, 150829, 150853, 150832, 150988, 191303, 191494, 151273, 150981, 150983, 150828, 151274, 151276, 150985, 151272, 37405, 150821, 151293, 151251, 193661, 150977)
GROUP BY
  repo_id, year, month
ORDER BY
  repo_id, year, month;
