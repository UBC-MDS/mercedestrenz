# Author: Spencer Gerlach
# Date: 2023-01-20
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
    >>> from mercedestrenz.data import load_sample_mercedes_listings
    >>> sample_mercedes_listings = load_sample_mercedes_listings()
    """
    with resources.path('mercedestrenz.datasets', 'mercedes.csv') as d:
        data = pd.read_csv(d, index_col=0)
        return data


# Author: Kelly Wu
# Date: 2023-01-19
def listing_search(data, budget=[0, np.Inf], model = "any", sort_feature = "odometer_mi", ascending = True, price_col = 'price_USD')-> pd.DataFrame():
    """
    Return the top listings that are within the budget specified by the user.

    The results are filtered by an optional input, model.
    The results are also sorted by ascending price and another the specified feature in the sort_feature parameter. 
    By default the sort_feature is lower mileage value, but user has the flexibility to choose another numeric attribute.
    Return an empty pandas dataframe when there is no listing that satisfies the criteria.
    
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
    price_col : string
        String value that indicates the column name of car price. The default is price_USD.

    Returns
    -------
    pandas.DataFrame
        A pandas dataframe of the sorted listings that matches user's expected budget range.
    
    Examples
    --------
    >>> # search listings within a price range
    >>> listing_search(data, budget=[2000, 20000], model = "any", sort_feature = "odometer_mi", ascending = True)
    >>> # search listings for a specific model and below a maximum price
    >>> listing_search(data, budget=20000, model = "gl-class", sort_feature = "odometer_mi", ascending = True)
    """

    # ======= Unit tests ==========
    # check input data is a pd.dataframe
    if type(data) != pd.DataFrame:
        raise Exception("The input dataset is not of Pandas DataFrame format")

    # check budget is either a flort/int or a list of float/int
    if type(budget) not in [float, int]: 
        if len(budget) == 2:
            for elem in budget:
                if type(elem) not in [float, int]:
                    raise Exception("The budget range boundaries should be floats or integers")
        else:
            raise Exception("Please specify your maximum budget using a number, or a range of budge using a list of numeric values.")

    # model= parameter input should be a string
    if type(model) != str:
            raise Exception("The model parameter should have a string as the input")
    
    # The string should correspond to a specific car model in the model column
    if ((model in data['model'].unique()) or model == 'any') == False:
        raise Exception("The specified car model does not exist in the dataframe provided")

    # sort_feature should be a string
    if type(sort_feature) != str:
        raise Exception("The input value for sort_feature parameter should be a string")
    
    # sort_feature should indicate a numeric column in the provided data frame
    numeric_cols = data.select_dtypes('number').columns.to_list()
    if sort_feature not in numeric_cols:
        raise Exception("The specified sort_feature should be a numeric column in the provided dataframe.")

    # ascending is either true or false
    if type(ascending) != bool:
        raise Exception("Please specify True or False in the ascending parameter")
    
    # price_col string
    if type(price_col) != str:
        raise Exception("Please specify the price column name using a string, or use the default value.")


    # ======= Function ==========
    
    # filter by budget
    if type(budget) in [float, int]: # max budget specified
        condition = data[price_col] <= budget
    else:
        condition = ((budget[0] <= data[price_col]) & (data[price_col] <= budget[1]))
    temp_df = data.loc[condition]

    # filter by model
    if model != "any":
        condition = data['model'] == model
        temp_df = temp_df.loc[condition]

    # sort by price & output
    result = temp_df.sort_values(by = [sort_feature, price_col], ascending = [ascending, True])

    # order output 
    priority_order = [price_col, 'model', sort_feature]
    remaining = list(set(data.columns) - set(priority_order))
    all_col = priority_order + remaining
    result = result.loc[:, all_col]

    return result
