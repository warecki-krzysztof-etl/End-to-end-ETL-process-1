{% snapshot product_snapshots %}

{{
    config(
        target_schema = 'public',
        unique_key = 'id',
        strategy = 'check',
        check_cols = ['cena_pln']
    )
}}

SELECT * FROM public.produkty

{% endsnapshot %}