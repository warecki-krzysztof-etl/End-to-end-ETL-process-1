{% macro get_discount(price_column, discount_percent) %}
    ({{price_column}} * (1.0 - {{discount_percent}} / 100.0))
{% endmacro %}

{% macro double_price(price) %}
    ({{price}} * 2.0)
{% endmacro %}