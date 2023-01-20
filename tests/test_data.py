# Author: Kelly Wu
# Date: 2023-01-19
from mercedestrenz.data import listing_search
import pandas as pd
import numpy as np

def test_listing_search():
    """Unit tests for listing_search function. """
    
    # Create a fictitious dataset for testing
    data = {'url':['www.a.ca', 'auto.com', 'benz.ca', 'cars.ca'],
        'condition':["good", 'average', 'average', 'new'],
        'price' : [50000, 20000, 80000, 90000],
        'model' : ['s-class', 'glk', 'gls', 'gls'],
        'odometer': [12000, 30000, 35000, 150000],
        'year': [2016, 2015, 2020, 2010]
        }
    df = pd.DataFrame(data)

    # Regular use cases
    t1 = listing_search(df, budget=50000, model = "glk", sort_feature = "odometer", ascending = True)
    assert type(t1) == pd.DataFrame, "The function did not return a Pandas Dataframe"
    assert t1.shape == (1,6), "Wrong number of listings returned"
    assert t1['model'].tolist() == ['glk'], "The outout was not filtered by model= parameter "

    assert set(t1.columns) == set(['url', 'price', 'model', 'odometer', 'condition', 'year']), "The dataframe does not contain the correct columns"

    t2 = listing_search(df, budget=[50000, 100000], model = "any", sort_feature = "year", ascending = False)
    assert t2.shape == (3,6), "Wrong number of listings returned"
    assert t2['model'].tolist() == ['gls', 's-class', 'gls'], "Wrong values returned by the function"
    assert t2['year'].tolist() == [2020, 2016, 2010], "Listings are not properly sorted by sort_feature and ascending parameter"

    # Raise error for wrong input values

    # wrong budget price range
    try:
        listing_search(df, budget=[0, 100, 10000], model = "any", sort_feature = "year", ascending = False)
    except Exception as e:
        # Check if the correct exception was raised
        assert str(e) == "Please specify your maximum budget using a number, or a range of budge using a list of numeric values.", f"Unexpected exception raised: {e}"
    else:
        # If no exception was raised, fail the test
        assert False, "Expected exception was not raised"
    
    # wrong input for model parameter
    try:
        listing_search(df, budget=[0, 80000], model = "450", sort_feature = "year", ascending = False)
    except Exception as e:
        assert str(e) == "The specified car model does not exist in the dataframe provided", f"Unexpected exception raised: {e}"
    else:
        assert False, "Expected exception was not raised"
    try:
        listing_search(df, budget=[0, 80000], model = 450, sort_feature = "year", ascending = False)
    except Exception as e:
        assert str(e) == "The model parameter should have a string as the input", f"Unexpected exception raised: {e}"
    else:
        assert False, "Expected exception was not raised"

    # wrong input for sort_feature parameter
    try:
        listing_search(df, budget=[0, 80000], model = 'gls', sort_feature = ['price', 'year'], ascending = False)
    except Exception as e:
        assert str(e) == "The input value for sort_feature parameter should be a string", f"Unexpected exception raised: {e}"
    else:
        assert False, "Expected exception was not raised"
    try:
        listing_search(df, budget=[0, 80000], model = 'gls', sort_feature = 'condition', ascending = False)
    except Exception as e:
        assert str(e) == "The specified sort_feature should be a numeric column in the provided dataframe.", f"Unexpected exception raised: {e}"
    else:
        assert False, "Expected exception was not raised"       

    # Wrong input value for ascending parameter
    try:
        listing_search(df, budget=[0, 80000], model = 'gls', sort_feature = 'odometer', ascending = "OK")
    except Exception as e:
        assert str(e) == "Please specify True or False in the ascending parameter", f"Unexpected exception raised: {e}"
    else:
        assert False, "Expected exception was not raised"  