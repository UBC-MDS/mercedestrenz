# Author: Morris Zhao
# Date: 2023-01-17

# from mercedestrenz.data import listing_search
from mercedestrenz.visualizations import plot_mercedes_price
import pandas as pd
import altair as alt
import numpy as np

# Create a small dataframe with one column named 'price' (just for testing).
df = pd.DataFrame(np.random.randint(10000, 500000, 1000), columns=['price'])
df['model'] = 'glb'

def test_input_model():
    """
    Test when input model is an integer, the function will throw an error
    """
    try:
        plot_mercedes_price(10, 450000, df, price_col = 'price')
    except Exception as e:
        # Check if the correct exception was raised
        assert str(e) == "The first input should be a string contain the specific model", f"Unexpected exception raised: {e}"
    else:
        # If no exception was raised, fail the test
        assert False, "Expected exception was not raised"

def test_input_price():
    """
    Test when input price is a string, the function will throw an error
    """
    try:
        plot_mercedes_price('glb', '400000', df, price_col = 'price')
    except Exception as e:
        # Check if the correct exception was raised
        assert str(e) == "The second input should be a number (the price of the car)", f"Unexpected exception raised: {e}"
    else:
        # If no exception was raised, fail the test
        assert False, "Expected exception was not raised"

def test_market_df():
    """
    Test when input market_df is a dataframe, the function will throw an error
    """
    try:
        plot_mercedes_price('glb', 400000, 1234, price_col = 'price')
    except Exception as e:
        # Check if the correct exception was raised
        assert str(e) == "The third input should be a pd.DataFrame", f"Unexpected exception raised: {e}"
    else:
        # If no exception was raised, fail the test
        assert False, "Expected exception was not raised"

def test_price_column():
    """
    Test if price column not in the data set, the function will throw an error
    """
    try:
        plot_mercedes_price('glb', 400000, df)
    except Exception as e:
        # Check if the correct exception was raised
        assert str(e) == "Please insert the name of the price column (e.g. plot_mercedes_price('glc',10,df,price_col='price_CAD')"
    else:
        # If no exception was raised, fail the test
        assert False, "Expected exception was not raised"

def test_model_column():
    """
    Test if model column not in the data set, the function will throw an error
    """
    try:
        plot_mercedes_price('glb', 400000, df, model_col = 'model 1', price_col = 'price')
    except Exception as e:
        # Check if the correct exception was raised
        assert str(e) == "Please insert the name of the model column"
    else:
        # If no exception was raised, fail the test
        assert False, "Expected exception was not raised"

def test_return():
    """
    Test whether the function returns a plot
    """
    if not isinstance(plot_mercedes_price('glb', 450000, df, price_col = 'price'), alt.LayerChart):
        raise Exception("Function did not return an Altair chart")