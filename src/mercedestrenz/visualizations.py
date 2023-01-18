# Author: Morris Zhao
# Date: 2023-01-12

# from data import listing_search
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
    
    # filter the data set for the specific model
    # model_df = listing_search(market_df, model = model)

    # Add current price to the data set
    market_df['x'] = price
    
    # Target column is price
    target_col = 'price'
    
    # Caculating the median of the market
    median = np.percentile(market_df['price'], 50)
    
    # different message will be send base on price
    if price > median:
        message = f"The input {target_col} = {price} is larger than the median of the market"
    else:
        message = f"The input {target_col} = {price} is smaller than the median of the market"
    
    # Define plot title
    plot_title = alt.TitleParams(
    f"Density Plot of Mercedes-Benz {model}",
    subtitle = message)

    # Create density plot for the specific model
    density_plot = alt.Chart(
        market_df, title = plot_title
    ).transform_density(
        target_col, as_=[target_col, 'density']
    ).mark_area(
        opacity=0.9
    ).encode(
        alt.X(f'{target_col}:Q', title="Price", 
              axis=alt.Axis(format='s', tickSize=0)),
        alt.Y('density:Q', title='Density', 
              axis=alt.Axis(labels=False, tickSize=0)),
        tooltip=f'{target_col}:Q'
    )
    
    # Create a line indicates where current car price is.
    line = alt.Chart(market_df).mark_rule(color='red', size=2).encode(x='x')
    
    # Combine the density plot and line
    final_plot = density_plot + line
    
    return final_plot
    