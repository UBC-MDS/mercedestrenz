# Author: Morris Zhao
# Date: 2023-01-12

from data import listing_search
import pandas as pd
import altair as alt

def plot_mercedes_price(model, price, market_df):
    """
    Plot a density plot of a specific Mercedes-Benz model to see where 
    the current vehicle's price falls within the distribution of prices 
    for that model in the market.
    
    Parameters
    ----------
    model : str
        The model of the vehicle.
    price : float
        The price of the vehicle.
    market_df : pandas.DataFrame
        Dataframe containing information on used Mercedes-Benz in the market.
    
    Returns
    -------
    altair.Chart
        Density plot of prices for the specified Mercedes-Benz model.
    
    Examples
    --------
    >>> from mercedestrenz.visualizations import plot_mercedes_price
    >>> plot_mercedes_price(model='S-Class', price=80000, market_df=market_df))
    >>> plot_mercedes_price(model='C-Class', price=10000, market_df=used_car_df))
    """
    # Test if inputs have correct type
    if type(model) != str:
        raise Exception('The first input should be a string contain the specific model')
    if type(price) != float and type(price) != int:
        raise Exception('The second input should be a number (the price of the car)')
    if not isinstance(market_df, pd.DataFrame):
        raise Exception('The third input should be a pd.DataFrame')