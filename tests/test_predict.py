# Author: Ty Andrews
# Date: 2023-01-20
from mercedestrenz.predict import predict_mercedes_price
from mercedestrenz.predict import load_mercedes_price_model
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib
import pytest

# test that passing valid values returns a float
def test_predict_mercedes_price():
    assert isinstance(
        predict_mercedes_price("e-class", 2015, 55_000, "fair", "silver"), float
    )


# test that passing data the wrong types raises an error
@pytest.mark.parametrize(
    "model, year, odometer_mi, condition, paint_color",
    [
        (1, 2015, 55_000, "fair", "silver"),  # bad model dtype
        ("e-class", "2015", 55_000, "fair", "silver"),  # wrong year dtype
        ("e-class", 2015, "55_000", "fair", "silver"),  # wrong odometer_mi dtype
        ("e-class", 2015, 55_000, 1, "silver"),  # wrong condition dtype
        ("e-class", 2015, 55_000, "fair", 1),  # wrong paint_color dtype
    ],
)
def test_predict_mercedes_price_wrong_types(
    model, year, odometer_mi, condition, paint_color
):
    with pytest.raises(TypeError):
        predict_mercedes_price(model, year, odometer_mi, condition, paint_color)


# test that passing incorrect condition values raises an error
@pytest.mark.parametrize("condition", ["not", "a", "new condition", "slightly old"])
def test_predict_mercedes_price_wrong_condition(condition):
    with pytest.raises(ValueError):
        predict_mercedes_price("e-class", 2015, 55_000, condition, "silver")


@pytest.mark.parametrize("model_version", ["v1"])
def test_load_mercedes_price_model_v1(model_version):
    model = load_mercedes_price_model(model_version)
    assert isinstance(model, Pipeline)
