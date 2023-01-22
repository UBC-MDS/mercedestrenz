# Author: Ty Andrews
# Date: 2023-01-20
from mercedestrenz.train import train_mercedes_price_prediction_model
from mercedestrenz.data import load_sample_mercedes_listings
from sklearn.pipeline import Pipeline
import pandas as pd
import pytest


def test_train_mercedes_price_prediction_model():
    # test that passing valid values returns a tuple

    raw_data = load_sample_mercedes_listings()
    assert isinstance(
        train_mercedes_price_prediction_model(
            raw_data, "v1", model_type="gradient_boosting", save_model=False, n_iter=1
        ),
        tuple,
    )


def test_incorrect_data_train_price_prediction():
    # test that passing invalid data raises an error

    raw_data = pd.DataFrame(
        {
            "model": ["c-class"],
            "year": [2019],
            "odometer_mi": [10000],
            "condition": ["good"],
            "paint_color": ["black"],
            "price_USD": [10000],
        }
    )
    with pytest.raises(ValueError):
        train_mercedes_price_prediction_model(
            raw_data, "v1", model_type="gradient_boosting", save_model=False, n_iter=1
        )
