{{ config(
    materialized = 'ephemeral'
)}}
 
SELECT 
    kategoria_ang,
    kategoria_pl,
    LOWER(opiekun_dzialu) AS supporter_email
FROM {{ref('category_dict')}}