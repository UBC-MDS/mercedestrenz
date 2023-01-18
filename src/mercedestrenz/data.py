# Author: Spencer Gerlach
# Date: 2023-01-12
from importlib import resources
import pandas as pd
import numpy as np

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
    >>> sample_mercedes_listings = get_listings()
    """


# Author: Kelly Wu
# Date: 2023-01-12
def listing_search(data, budget=[0, np.Inf], model = "any", sort_feature = "odometer", ascending = True)-> pd.DataFrame():
    """
    Return the top listings that are within the budget specified by the user.

    The results are filtered by an optional input, model.
    The results are also sorted by ascending price and another the specified feature in the sort_feature parameter. 
    By default the sort_feature is lower mileage value, but user has the flexibility to choose another numeric attribute.
    Return an empty pandas dataframe when there is no listing that satisfies the criteria and print a warning message.
    
    Parameters
    ----------
    data : dataframe
        The input dataframe.
    budget : float or int,  or list of float or int
        The maximum budget, or the range of budget when passing a list.
    model : string
        The model of the car that the user is interested in. The default is to include listings of any model.
    sort_feature : string
        The numeric variable that the user is interested in using to sort the result. The default value is to sort by odometer value.
    ascending : bool
        Boolean value that indicate whether the sort is ascending. The default value is True.

    Returns
    -------
    pandas.DataFrame
        A pandas dataframe of the sorted listings that matches user's expected budget range.
    
    Examples
    --------
    >>> from mercedestrenz.mercedestrenz import listing_search
    >>> result = listing_search(data, budget=[2000, 20000], model = "any", sort_feature = "odometer", ascending = True)
    >>> result.head()
    #to be completed with exmaple output
    """
    pass


   