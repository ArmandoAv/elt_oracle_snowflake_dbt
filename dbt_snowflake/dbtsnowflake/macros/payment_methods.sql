{% macro column_values(column_name, table_name) %}

    {% set payment_methods_query %}

        SELECT {{ column_name }}
        FROM   {{ table_name }}
        GROUP BY 1
        ORDER BY 1

    {% endset %}

    {% set results = run_query(payment_methods_query) %}

    {% if execute %}

        {% set results_list = results.columns[0].values() %}

    {% else %}

        {% set results_list = [] %}
        
    {% endif %}

{{ return(results_list) }}

{% endmacro %}

{% macro payment_methods() %}

	{{ return(column_values('payment_method', ref('seed_payments'))) }}

{% endmacro %}
