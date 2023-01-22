# Author: Ty Andrews
# Date: 2023-01-12
import pandas as pd
from importlib import resources
import joblib

from sklearn.model_selection import cross_validate
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import RandomizedSearchCV


def train_mercedes_price_prediction_model(
    data: pd.DataFrame,
    model_version: str,
    model_type: str = "gradient_boosting",
    n_iter: int = 25,
    cv_results={},
    save_model: bool = False,
    overwrite_version: bool = False,
):
    """Trains a model to predict the price of a Mercedes-Benz given the year,

    Parameters
    ----------
    data : pd.DataFrame
        The raw used mercedes data. Must contain columns for model, year, condition, odometer_mi, paint_color, and price_USD.
    model_version : str
        The version of the model to train and subsequently save.
    model_type : str, optional
        The type of model to use to train on the data, by default "gradient_boosting"
    n_iter : int, optional
        How many iterations of randomized search to do during tuning, by default 25
    cv_results : dict, optional
        Pass existing dictionary of results to have these results appended, by default {}
    save_model : bool, optional
        Whether to save a version of the model, by default False
    overwrite_version : bool, optional
        If a version of that name already exists use this to overwrite it, by default False

    Returns
    -------
    Tuple[model, cv_results]
        The best performing model and the results of the cross validation.

    Raises
    ------
    ValueError
        If the data does not contain the required columns.

    Examples
    --------
    >>> from mercedestrenz.modelling import train_mercedes_price_prediction_model
    >>> model, results = train_mercedes_price_prediction_model(data, "v2", save_model=False)
    """

    if (
        set(
            ["model", "year", "condition", "odometer_mi", "paint_color", "price_USD"]
        ).issubset(data.columns)
        is False
    ):

        raise ValueError(
            "data must contain columns for model, year, condition, odometer_mi, paint_color, and price_USD"
        )

    else:
        train_data = data.loc[
            :, ["model", "year", "condition", "odometer_mi", "paint_color", "price_USD"]
        ]

    if train_data.isnull().values.any():
        print("Input train_data has null values, dropping any rows with null values.")
        num_samples_before = train_data.shape[0]
        train_data = train_data.dropna()
        num_samples_after = train_data.shape[0]
        print(
            f"Removed {num_samples_before - num_samples_after} rows. {len(train_data)} rows remaining."
        )

    # put the primary metric first for what the model is refit to with all the data
    # at the end of randomized search
    scoring_metrics = ["neg_root_mean_squared_error", "r2"]

    numeric_features = ["year", "odometer_mi"]
    ordinal_features = ["condition"]
    categorical_features = ["model", "paint_color"]

    target = "price_USD"

    X_train = train_data.drop(columns=[target])
    y_train = train_data[target]

    columntransformer = make_column_transformer(
        numeric_features, ordinal_features, categorical_features
    )

    model = make_model(model_type)

    param_grid = get_random_search_param_grid(model_type)

    pipe = make_pipeline(columntransformer, model)

    model_random_search = RandomizedSearchCV(
        pipe,
        param_distributions=param_grid,
        scoring=scoring_metrics,
        refit=scoring_metrics[0],
        n_jobs=-1,
        n_iter=n_iter,
        cv=5,
        return_train_score=True,
        random_state=42,
        verbose=2,
    )

    model_random_search.fit(X_train, y_train)

    best_model = model_random_search.best_estimator_

    model_cv = cross_validate(
        best_model,
        X_train,
        y_train,
        cv=5,
        scoring=scoring_metrics,
        return_train_score=True,
    )

    print(f"Best model: {model_random_search.best_params_}")
    print(
        f"Best model train {scoring_metrics[0]}: {model_random_search.cv_results_[f'mean_train_{scoring_metrics[0]}'][model_random_search.best_index_]:.1f}"
    )
    print(
        f"Best model test {scoring_metrics[0]}: {model_random_search.cv_results_[f'mean_test_{scoring_metrics[0]}'][model_random_search.best_index_]:.2}f"
    )

    cv_results[model_type] = pd.DataFrame(model_cv).agg(["mean", "std"]).round(3).T

    if save_model is True:
        export_mercedes_price_model(best_model, model_version, overwrite_version)

    return best_model, cv_results


def make_model(model_type: str):
    """Makes a model for the mercedes price prediction model

    Parameters
    ----------
    model_type : str
        What type of model to use

    Returns
    -------
    Model
        A model for the mercedes price prediction model
    """

    if model_type == "gradient_boosting":

        model = GradientBoostingRegressor(loss="squared_error", random_state=42)

    else:
        raise ValueError(f"model_type {model_type} not recognized")

    return model


def get_random_search_param_grid(model_type: str):
    """Gets a random search parameter grid for the mercedes
    price prediction model

    Parameters
    ----------
    model_type : str
        What type of model to use

    Returns
    -------
    dict
        A random search parameter grid for the mercedes price prediction model
    """

    if model_type == "gradient_boosting":

        param_grid = {
            "gradientboostingregressor__n_estimators": [150, 200, 250],
            "gradientboostingregressor__max_depth": [3, 5, 7, 9],
            "gradientboostingregressor__min_samples_split": [2, 3, 4, 5],
            "gradientboostingregressor__min_samples_leaf": [1, 2, 3, 4],
            "gradientboostingregressor__subsample": [0.5, 0.6, 0.8],
        }

    else:
        raise ValueError(f"model_type {model_type} not recognized")

    return param_grid


def make_column_transformer(numeric_features, ordinal_features, categorical_features):
    """Makes a column transformer for the mercedes price prediction model

    Parameters
    ----------
    numeric_features : list
        List of numeric features to include in the model
    ordinal_features : list
        List of ordinal features to include in the model
    categorical_features : list
        List of categorical features to include in the model

    Returns
    -------
    ColumnTransformer
        A column transformer for the mercedes price prediction model
    """

    columntransformer = ColumnTransformer(
        [
            ("scaling", StandardScaler(), numeric_features),
            (
                "onehot",
                OneHotEncoder(
                    sparse_output=False,
                    handle_unknown="infrequent_if_exist",
                    min_frequency=5,
                ),
                categorical_features,
            ),
            (
                "ordinal",
                OrdinalEncoder(
                    categories=[
                        [
                            "salvage",
                            "used",
                            "fair",
                            "good",
                            "excellent",
                            "like new",
                            "new",
                        ]
                    ]
                ),
                ordinal_features,
            ),
        ]
    )

    return columntransformer


def export_mercedes_price_model(model_pipeline, version="v1", overwrite=False):
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
        if d.exists() and overwrite is False:
            raise ValueError(
                f"Model version {version} already exists. Set overwrite=True to overwrite."
            )
        joblib.dump(model_pipeline, d)
        print("Model saved to: ", d)
