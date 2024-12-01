{{ 
    config(
        materialized = 'incremental', 
        on_schema_change='fail',
        cluster_by=['to_date(REVIEW_DATE)'],
        pre_hook = [
            "{{ delete_records(var('start_date', '1900-01-01 00:00:00'), var('end_date', '1900-01-01 23:59:59')) }}"
        ]
    ) 
}}

WITH src_reviews AS (
    SELECT * 
    FROM   {{ ref('src_reviews') }} 
) 
SELECT * 
FROM   src_reviews 
WHERE review_text is not null

{% if is_incremental() %}

  {% set start_date = var("start_date", '1900-01-01 00:00:00') %}
  {% set end_date = var("end_date", '1900-01-01 23:59:59') %}

  {% if start_date != '1900-01-01 00:00:00' and end_date != '1900-01-01 23:59:59' %}

    {{ log('Loading ' ~ this ~ ' incrementally (start_date: ' ~ var("start_date") ~ ', end_date: ' ~ var("end_date") ~ ')', info=True) }}
    AND review_date >= '{{ var("start_date") }}'
    AND review_date <= '{{ var("end_date") }}'

  {% else %}

    {{ log('Loading ' ~ this ~ ' incrementally (all missing dates)', info=True)}}
    AND review_date > (select max(review_date) from {{ this }})

  {% endif %}

{% endif %}
