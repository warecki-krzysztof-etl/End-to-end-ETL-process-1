{% macro asset_shelf(price_column) %}
    (CASE 
        WHEN {{price_column}} >= 100.0
            THEN 'Premium'
        WHEN {{price_column}} >= 50.0 
            THEN 'Standard'
        WHEN {{price_column}} < 50.0 
            THEN 'Budget'
    END)

{% endmacro %}