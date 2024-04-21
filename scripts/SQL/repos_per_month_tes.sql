WITH RepoCreation AS (
    SELECT
        DATE_TRUNC('month', CAST(repo_added AS TIMESTAMP)) AS creation_month,
        COUNT(*) AS repo_count  -- Counting all entries per month
    FROM
        augur_data.repo
    WHERE
        repo_git LIKE '%github.com/curl/%'  -- Ensuring correct syntax for LIKE
        AND repo_added IS NOT NULL  -- Making sure we exclude NULL repo_added dates
    GROUP BY
        DATE_TRUNC('month', CAST(repo_added AS TIMESTAMP))
),
MonthlyCumulative AS (
    SELECT
        series.month,
        COALESCE(SUM(rc.repo_count) OVER (ORDER BY series.month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 0) AS cumulative_repos
    FROM
        (SELECT generate_series(DATE_TRUNC('month', '2016-01-01'::date), 
                                DATE_TRUNC('month', '2024-05-01'::date), 
                                '1 month'::interval) AS month) AS series
    LEFT JOIN RepoCreation rc
    ON series.month = rc.creation_month
)
SELECT
    month,
    cumulative_repos
FROM
    MonthlyCumulative
ORDER BY
    month;
