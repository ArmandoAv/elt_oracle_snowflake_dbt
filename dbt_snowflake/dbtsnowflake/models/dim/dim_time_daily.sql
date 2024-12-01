WITH date_range AS (
   SELECT 
        TO_DATE(DATEADD(DAY, SEQ4(), '2009-01-01')) AS date
    FROM TABLE(GENERATOR(ROWCOUNT => 33237))
)

SELECT
    date,
    DAY(date) AS day,
    MONTH(date) AS month,
    YEAR(date) AS year,
    DAYOFWEEK(date) + 1 AS day_week,
    QUARTER(date) AS quarter,
    MONTHNAME(date) AS month_name,
    DATE_TRUNC('month', date) :: date AS first_day_month,
    LAST_DAY(date, 'month') :: date AS last_day_month
FROM date_range
