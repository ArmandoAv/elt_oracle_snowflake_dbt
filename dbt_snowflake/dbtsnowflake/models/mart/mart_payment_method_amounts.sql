{{ 
    config(
        materialized = 'table', 
        ) 
}} 

{% set payment_methods = payment_methods() %}

SELECT
    listing_id,
    nights_booked,
    {% for payment_method in payment_methods %}
        sum(case when payment_method = '{{payment_method}}' then amount end) :: NUMERIC(10,2) as {{payment_method}}_amount
        {% if not loop.last %},{% endif %}
    {% endfor %}
FROM 
    {{ ref('seed_payments') }}
GROUP BY 
    1, 2
