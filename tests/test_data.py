# Author: Kelly Wu
# Date: 2023-01-19
from mercedestrenz.data import listing_search
import pandas as pd
import numpy as np

def test_listing_search():
    """Unit tests for listing_search function. """
    
    # Create a fictitious dataset for testing
    data = {
        'condition':["good", 'average', 'average', 'new'],
        'price_USD' : [50000, 20000, 80000, 90000],
        'model' : ['s-class', 'glk', 'gls', 'gls'],
        'odometer_mi': [12000, 30000, 35000, 150000],
        'year': [2016, 2015, 2020, 2010]
        }
    df = pd.DataFrame(data)

    # Regular use cases
    t1 = listing_search(df, budget=50000, model = "glk", sort_feature = "odometer_mi", ascending = True)
    assert type(t1) == pd.DataFrame, "The function did not return a Pandas Dataframe"
    assert t1.shape == (1,5), "Wrong number of listings returned"
    assert t1['model'].tolist() == ['glk'], "The outout was not filtered by model= parameter "

    assert set(t1.columns) == set(['price_USD', 'model', 'odometer_mi', 'condition', 'year']), "The dataframe does not contain the correct columns"

    t2 = listing_search(df, budget=[50000, 100000], model = "any", sort_feature = "year", ascending = False)
    assert t2.shape == (3,5), "Wrong number of listings returned"
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

    try:
        listing_search(df, budget=[0, '80000'], model = 450, sort_feature = "year", ascending = False)
    except Exception as e:
        assert str(e) == "The budget range boundaries should be floats or integers", f"Unexpected exception raised: {e}"
    else:
        assert False, "Expected exception was not raised"
        
    try:
        listing_search(df, budget=['0', 80000], model = 450, sort_feature = "year", ascending = False)
    except Exception as e:
        assert str(e) == "The budget range boundaries should be floats or integers", f"Unexpected exception raised: {e}"
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
        listing_search(df, budget=[0, 80000], model = 'gls', sort_feature = 'odometer_mi', ascending = "OK")
    except Exception as e:
        assert str(e) == "Please specify True or False in the ascending parameter", f"Unexpected exception raised: {e}"
    else:
        assert False, "Expected exception was not raised"  

    # invalid input dataset type
    try:
        listing_search(data, budget=[0, 100, 10000], model = "any", sort_feature = "year", ascending = False)
    except Exception as e:
        # Check if the correct exception was raised
        assert str(e) == "The input dataset is not of Pandas DataFrame format", f"Unexpected exception raised: {e}"
    else:
        # If no exception was raised, fail the test
        assert False, "Expected exception was not raised"

# Author: Spencer Gerlach
# Date: 2023-01-19
from mercedestrenz.data import load_sample_mercedes_listings


def test_load_sample_mercedes_listings():
    """Tests for correct loading of sample data"""
    
    # Wrong columns
    expected_num_columns = 16
    actual_num_columns = len(load_sample_mercedes_listings().columns)
    assert actual_num_columns == expected_num_columns, "Incorrect number of columns returned."

    # Wrong rows
    expected_num_rows = 8553
    actual_num_rows = len(load_sample_mercedes_listings())
    assert actual_num_rows == expected_num_rows, "Incorrect number of rows returned."

    # No dataframe returned
    assert load_sample_mercedes_listings() is not None, "Dataframe is not being returned by the function."

    # Not pd.DataFrame type
    assert type(load_sample_mercedes_listings()) is pd.DataFrame, "Function does not return a pandas dataframe."

    # Wrong column names
    expected_col_names = ['price_USD', 'condition', 'paint_color', 'model', 'odometer_mi', 'year',
       'num_cylinders', 'fuel', 'transmission', 'drive', 'size', 'type',
       'state', 'VIN', 'title_status', 'description']
    actual_col_names = load_sample_mercedes_listings().columns
    assert sum(expected_col_names == actual_col_names) == 16, "Column names not imported correctly (incorrect names or sequencing)."
