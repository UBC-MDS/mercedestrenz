# Author: Ty Andrews
# Date: 2023-01-12


def predict_mercedes_price(
    year: int, model: str, condition: str, num_cylinders: int
) -> float:
    """Predicts the price in USD of a Mercedes-Benz given the year, model,
    condition, and number of cylinders.

    Uses a pre-trained model built into the package to predict the price of the
    mercedes. The model was trained on data from 1990 to 2022.

    Parameters
    ----------
    year : int
        The year the Mercedes-Benz was made.
    model : str
        The model of the Mercedes-Benz.
    condition : str
        The condition of the Mercedes-Benz.
        Options: 'new', 'like new', 'excellent', 'good', 'fair', 'salvage'.
    num_cylinders : int
        The number of cylinders in the Mercedes-Benz.
            Options: 3, 4, 5, 6, 8, 10, 12.

    Returns
    -------
    float
        The predicted price of the Mercedes-Benz.

    Raises
    ------
    ValueError
        If the year is not between 1990 and 2022.
    ValueError
        If the model is not in the training set.
    ValueError
        If the condition is not one of the following:
            'new', 'like new', 'excellent', 'good', 'fair', 'salvage'.
    ValueError
        If the number of cylinders is not one of the following:
            3, 4, 5, 6, 8, 10, 12.

    Examples
    --------
    >>> from mercedestrenz.modelling import predict_mercedes_price
    >>> predict_mercedes_price(2020, 'C-Class', 'new', 4)
    """

    return -1.0
