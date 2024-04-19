WITH initial_issues AS (
    SELECT
        COUNT(*) AS initially_open
    FROM
        augur_data.issues
    WHERE
        repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%github.com/curl/%')
        AND created_at < '2016-01-01'
        AND (closed_at IS NULL OR closed_at > '2016-01-01')
),
monthly_data AS (
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        COUNT(*) AS opened,
        0 AS closed
    FROM
        augur_data.issues
    WHERE
        repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%github.com/curl/%')
        AND created_at BETWEEN '2016-01-01' AND '2024-01-01'
    GROUP BY DATE_TRUNC('month', created_at)

    UNION ALL

    SELECT
        DATE_TRUNC('month', closed_at) AS month,
        0 AS opened,
        COUNT(*) AS closed
    FROM
        augur_data.issues
    WHERE
        repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%github.com/curl/%')
        AND issue_state = 'closed'
        AND closed_at IS NOT NULL
        AND closed_at BETWEEN '2016-01-01' AND '2024-06-01'
    GROUP BY DATE_TRUNC('month', closed_at)
),
aggregated_data AS (
    SELECT
        month,
        SUM(opened) AS total_opened,
        SUM(closed) AS total_closed
    FROM
        monthly_data
    GROUP BY month
),
running_totals AS (
    SELECT
        month AS issue_month,
        SUM(total_opened - total_closed) OVER (ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS net_open_issues
    FROM
        aggregated_data
)
SELECT
    issue_month,
    (SELECT initially_open FROM initial_issues) + net_open_issues AS running_total_open_issues
FROM
    running_totals
ORDER BY issue_month;
