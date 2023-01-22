# Author: Ty Andrews
# Date: 2023-01-12
import pandas as pd
from importlib import resources
import joblib


def predict_mercedes_price(
    model: str,
    year: int,
    odometer_mi: int,
    condition: str,
    paint_color: str,
    version="v1",
) -> int:
    """Predicts the price in USD of a Mercedes-Benz given the year, model,
    condition, paint color and odometer reading.

    Uses a pre-trained model built into the package to predict the price of the
    mercedes. The model was trained on data from 1990 to 2022.

    Parameters
    ----------
    model : str
        The model of the Mercedes-Benz.
    year : int
        The year the Mercedes-Benz was made.
    condition : str
        The condition of the Mercedes-Benz.
        Options: 'new', 'like new', 'excellent', 'good', 'fair', 'salvage'.
    odometer_mi : int
        The odometer reading in miles.
    paint_color : str
        The color of the paint.
    version : str, optional
        Model version to use if multiple available, by default "v1".

    Returns
    -------
    int
        The predicted price of the Mercedes-Benz in USD.

    Raises
    ------
    ValueError
        If the year is not between 1929 and 2021.
    ValueError
        If the model is not in the training set.
    ValueError
        If the condition is not one of the following:
            'new', 'like new', 'excellent', 'good', 'fair', 'used', 'salvage'.

    Examples
    --------
    >>> from mercedestrenz.modelling import predict_mercedes_price
    >>> predict_mercedes_price("e-class", 2015, 55_000, "fair", "silver")
    """

    if type(model) is not str:
        raise TypeError("model must be a string")
    if type(year) is not int:
        raise TypeError("year must be an integer from 1929 to 2021")
    if type(odometer_mi) is not int:
        raise TypeError("odometer_mi must be an integer")
    if (type(condition) is not str):
        raise TypeError(
            "condition must be of type str and one of 'salvage', 'used', 'fair', 'good', 'excellent', 'like new', 'new'"
        )
    if (condition
        not in ["salvage", "used", "fair", "good", "excellent", "like new", "new"]
    ):
        raise ValueError(
            "condition must be one of 'salvage', 'used', 'fair', 'good', 'excellent', 'like new', 'new'"
        )
    if type(paint_color) is not str:
        raise TypeError("paint_color must be a string, if unsure use 'unknown'")
    if type(version) is not str:
        raise TypeError("version must be a string of form 'vX'")

    price_model = load_mercedes_price_model(version)

    price_prediction = price_model.predict(
        pd.DataFrame(
            {
                "model": [model],
                "year": [year],
                "odometer_mi": [odometer_mi],
                "condition": [condition],
                "paint_color": [paint_color],
            }
        )
    )

    return round(float(price_prediction[0]), 2)


def export_mercedes_price_model(model_pipeline, version="v1"):
    """Exports the sklearn model pipeline for mercedes price prediction

    Parameters
    ----------
    model_pipeline : PipeLine
        sklearn pipeline with the model and preprocessing steps
    version : str, optional
        What to tag the model version by. By default "v1"
    """

    model_name = f"mercedes_price_prediction_{version}.joblib"
    with resources.path("mercedestrenz.models", model_name) as d:

        joblib.dump(model_pipeline, d)


def load_mercedes_price_model(version="v1"):
    """Loads the sklearn model for mercedes price prediction

    Parameters
    ----------
    version : str, optional
        Model version to use if multiple available, by default "v1"

    Returns
    -------
    Pipeline
        A sklearn pipeline with the model and preprocessing steps

    Raises
    ------
    FileNotFoundError
        If the model version is not found.
    """

    model_name = f"mercedes_price_prediction_{version}.joblib"
    with resources.path("mercedestrenz.models", model_name) as d:

        try:
            mercedes_price_model = joblib.load(d)
        except FileNotFoundError as e:
            with resources.path("mercedestrenz", "models") as p:
                raise FileNotFoundError(
                    f"Model version {version} not found. Available models: \n{list(p.glob('*.joblib'))}"
                )

    return mercedes_price_model
