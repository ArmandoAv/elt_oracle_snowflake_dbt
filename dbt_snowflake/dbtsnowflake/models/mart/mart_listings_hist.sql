{{ 
    config(
        materialized = 'table', 
        ) 
}} 

WITH mart_listings AS ( 
    SELECT *
    FROM   {{ ref('src_raw_listings') }}
)
SELECT 
    id AS listing_id, 
    name AS listing_name, 
    room_type, 
    CASE
        WHEN minimum_nights = 0 THEN 1 
        ELSE minimum_nights 
    END AS minimum_nights, 
    host_id, 
    REPLACE(price,'$') :: NUMBER(10,2) AS price, 
    created_at,
    dbt_valid_from AS start_date, 
    dbt_valid_to AS end_date,
    CASE
        WHEN dbt_valid_to IS NULL THEN 'Y'
        ELSE 'N'
    END AS is_current
FROM 
    mart_listings
