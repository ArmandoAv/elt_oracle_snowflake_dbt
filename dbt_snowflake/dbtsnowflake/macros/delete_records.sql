{% macro delete_records(start_date, end_date) %}

    {% if start_date != '1900-01-01 00:00:00' and end_date != '1900-01-01 23:59:59' %}

        {{ log('Deleted records from ' ~ start_date ~ ' to ' ~ end_date, info=True) }}
        DELETE FROM {{ this }} 
        WHERE review_date >= '{{ start_date }}' 
        AND review_date <= '{{ end_date }}'

    {% else %}
        {{ log('Skip delete because it is not a reprocess', info=True) }}

    {% endif %}

{% endmacro %}
