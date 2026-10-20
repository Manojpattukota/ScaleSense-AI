

USE scalesense_ai;

-- Daily traffic summary
SELECT
    day_of_month,
    COUNT(*) AS total_minutes,
    SUM(request_count) AS total_requests,
    ROUND(AVG(request_count), 2) AS avg_requests_per_minute,
    MAX(request_count) AS peak_requests_per_minute
FROM traffic_data
GROUP BY day_of_month
ORDER BY day_of_month;

-- Hourly traffic summary
SELECT
    hour_of_day,
    COUNT(*) AS total_minutes,
    SUM(request_count) AS total_requests,
    ROUND(AVG(request_count), 2) AS avg_requests_per_minute,
    MAX(request_count) AS peak_requests_per_minute
FROM traffic_data
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- Identify high-traffic minutes (95th percentile threshold)
SELECT
    COUNT(*) AS total_minutes,
    SUM(CASE WHEN request_count > 84 THEN 1 ELSE 0 END)
        AS high_traffic_minutes,
    ROUND(
        100.0 * SUM(CASE WHEN request_count > 84 THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS high_traffic_percentage,
    MAX(request_count) AS highest_requests_per_minute
FROM traffic_data;

-- Power BI hourly summary
SELECT
    hour_of_day,
    SUM(request_count) AS total_requests,
    ROUND(AVG(request_count), 2) AS avg_requests_per_minute,
    MAX(request_count) AS peak_requests_per_minute,
    SUM(CASE WHEN request_count > 84 THEN 1 ELSE 0 END)
        AS spike_minutes,
    ROUND(
        100.0 * SUM(CASE WHEN request_count > 84 THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS spike_percentage
FROM traffic_data
GROUP BY hour_of_day
ORDER BY hour_of_day;
