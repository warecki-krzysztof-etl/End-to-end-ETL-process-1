{{ config(materialized = 'table') }}

SELECT 
    p.tytul, 
    p.cena_pln,
    k.kategoria_pl
FROM public.produkty p
LEFT JOIN {{ ref('stg_categories') }} k
    ON p.kategoria = k.kategoria_ang