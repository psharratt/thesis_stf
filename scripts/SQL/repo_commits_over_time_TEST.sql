SELECT *
FROM augur_data.commits
WHERE repo_id = 191494;


SELECT
  EXTRACT(YEAR FROM CAST(cmt_author_date AS DATE)) AS year,
  EXTRACT(MONTH FROM CAST(cmt_author_date AS DATE)) AS month,
  COUNT(*) AS total_commits
FROM
  augur_data.commits
WHERE
  repo_id = 191540 -- GStreamer repo...
GROUP BY
  year,
  month
ORDER BY
  year,
  month;

SELECT
  EXTRACT(YEAR FROM CAST(cmt_author_date AS DATE)) AS year,
  EXTRACT(MONTH FROM CAST(cmt_author_date AS DATE)) AS month,
  COUNT(*) AS total_commits
FROM
  augur_data.commits
WHERE
  repo_id = 151273 -- rattler-build
GROUP BY
  year,
  month
ORDER BY
  year,
  month;
