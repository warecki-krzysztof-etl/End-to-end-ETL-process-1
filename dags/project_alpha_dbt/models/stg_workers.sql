{{ config(materialized = 'ephemeral') }}

SELECT
    id_pracownika,
    imie,
    dzial,
    CASE
        WHEN waluta = 'EUR' THEN kwota * 4.3
        ELSE kwota
    END AS pensja_w_pln
FROM {{ ref('workers') }}