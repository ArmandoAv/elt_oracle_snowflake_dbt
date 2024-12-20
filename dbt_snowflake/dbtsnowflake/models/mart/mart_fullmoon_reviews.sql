{{ 
    config(
        materialized = 'table', 
        ) 
}} 
 
WITH fct_reviews AS ( 
    SELECT * 
    FROM   {{ ref('fct_reviews') }} 
), 
     full_moon_dates AS ( 
    SELECT * 
    FROM   {{ ref('seed_full_moon_dates') }} 
) 
SELECT
    rev.*, 
    CASE 
        WHEN fm.full_moon_date IS NULL THEN 'not full moon' 
        ELSE 'full moon' 
    END AS is_full_moon 
FROM fct_reviews rev 
LEFT JOIN full_moon_dates fm 
ON TO_DATE(rev.review_date) = DATEADD(DAY, 1, fm.full_moon_date)
