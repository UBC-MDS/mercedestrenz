from importlib import resources
import pandas as pd

def get_listings():
    """
    Retrieves a dataframe containing sample data of used Mercedez Benz vehicles. 
    The function returns a pandas dataframe of all sample listings.

    Returns
    -------
    pandas.DataFrame
        A pandas dataframe of all listings contained in the package's sample data.
    
    Examples
    --------
    >>> from mercedeztrenz/datasets import get_listings
    >>> output_pandas_df = get_listings()
    """