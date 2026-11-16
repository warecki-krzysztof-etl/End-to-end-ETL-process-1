{{ config(materialized = 'table') }}

SELECT 
    id,
    tytul,
    cena_usd,
    {{asset_shelf('cena_usd')}} as "Price Tag"
FROM public.produkty