{% macro variables_jinja_dbt() %}

    {% set variable_jinja = "Master" %}
    {{ log("Hello: " ~ variable_jinja, info=True) }}

    {{ log("Hello DBT user: " ~ var("user_name", "No user name is set") ~ "!", info=True)}}

{% endmacro %}
