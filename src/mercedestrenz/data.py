def listing_search(max_price=30000, region = "any", model = "any", sort_feature = "odometer", ascending = True):
    """
    Return the top listings that are within the budget specified by the user, sorted by price from lowest to highest.
    The results are filtered by optional input, region and model.
    The results are also sorted by ascending price and another the specified feature in the sort_feature parameter. 
    By default the sort_feature is lower mileage value, but user has the flexibility to choose another numeric attribute.

    Return an empty pandas dataframe when there is no listing that satisfies the criteria and print a warning message.
    
    Parameters
    ----------
    max_price : float
        The maximum of the budget range.
    region : string
        The region of the listing. The default is to include listings from any region.
    model : string
        The model of the car that the user is interested in. The default is to include listings of any model.
    sort_feature : string
        The numeric variable that the user is interested in using to sort the result. The default value is to sort by odometer value.
    ascending : bool
        Boolean value that indicate whether the sort is ascending. The default value is True.

    Returns
    -------
    pandas.DataFrame
        A pandas dataframe of the sorted listings that matches user's expected price range.
    
    Examples
    --------
    >>> from mercedestrenz.mercedestrenz import listing_search
    >>> listing_search(max_price=30000, region = "any", model = "S-class", sort_feature = "odometer", ascending = True)
    """
    pass