{{ config(materialized = 'table')}}
SELECT 
    dzial,
    COUNT(id_pracownika) AS "Liczba Pracowników",
    AVG(pensja_w_pln) AS "Średnia zarobków w Polskich Złotych"
FROM {{ ref('stg_workers') }}
    GROUP BY dzial