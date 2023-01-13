def plot_benz(model, price, market_df):
    """
    Plot a density plot of a specific Mercedes-Benz model to see where 
    the current vehicle's price falls within the distribution of prices 
    for that model in the market.
    
    Parameters
    ----------
    model : str
        The model of the vehicle intersted.
    price : float
        The price of the vehicle intersted.
    market_df : pandas.DataFrame
        Dataframe containing information on used Mercedes-Benz in the market.
    
    Returns
    -------
    altair.Chart
        Density plot of prices for the specified Mercedes-Benz model.
    
    Examples
    --------
    >>> from mercedestrenz.visualizations import plot_benz
    >>> plot_benz(model='S-Class', price=80000, market_df=market_df))
    """