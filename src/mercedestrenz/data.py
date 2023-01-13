# Author: Spencer Gerlach
# Date: 2023-01-12
from importlib import resources
import pandas as pd

def load_sample_mercedes_listings()-> pd.DataFrame():
    """
    Retrieves a dataframe containing sample data of used Mercedez Benz vehicles. 
    The function returns a pandas dataframe of all sample listings.

    Returns
    -------
    pandas.DataFrame
        A pandas dataframe of all listings contained in the package's sample data.
    
    Examples
    --------
    >>> from mercedestrenz.datasets import get_listings
    >>> output_pandas_df = get_listings()
    """