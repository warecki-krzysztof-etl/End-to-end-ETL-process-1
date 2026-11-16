import pandas as pd
from dags.pipeline import exchange_to_pln

def test_exchange_to_pln():
    dane_testowe = pd.DataFrame({
            "cena_usd": [10.0, 5.0, 0.0]
        })

    final_pd = exchange_to_pln(dane_testowe)

    assert "cena_pln" in final_pd.columns, "Missing column \'cena_pln\'!"

    assert final_pd["cena_pln"][0] == 40.0, "Fault"

    assert final_pd["cena_pln"][1] == 20.0, "Fault"

    assert final_pd["cena_pln"][2] == 0.0, "Fault"