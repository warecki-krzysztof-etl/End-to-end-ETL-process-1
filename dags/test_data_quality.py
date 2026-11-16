import pandas as pd
import pytest
def test_no_above_zero_products():
    data = pd.read_parquet('/tmp/silver_layer/', engine = 'pyarrow')
    assert data['cena_usd'].min() >= 0, "Warning! Bad data [PRODUCTS WITH PRICE ABOVE 0$]"

def test_empty_titles():
    data = pd.read_parquet('/tmp/silver_layer/', engine = 'pyarrow')
    assert data['tytul'].isnull().sum() == 0, "Warning! Bad data [EMPTY TITLES]"
