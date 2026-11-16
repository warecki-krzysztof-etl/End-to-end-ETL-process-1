{{ config(
    materialized = 'incremental',
    unique_key = 'id'
)}}

SELECT 
    id,
    tytul,
    cena_usd
FROM public.produkty

{% if is_incremental() %}
        WHERE id > (SELECT max(id) FROM {{this}})
{% endif %}