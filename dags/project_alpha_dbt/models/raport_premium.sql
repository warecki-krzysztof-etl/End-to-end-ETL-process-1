{{ config( materialized = 'table' )}}

SELECT
    id,
    tytul,
    kategoria,
    cena_pln,
    {{get_discount('cena_pln', 10.0)}} as "Discounted Prices",
    {{double_price('cena_usd')}} as "Doubled Price"
FROM public.produkty
WHERE cena_pln > 200.0
