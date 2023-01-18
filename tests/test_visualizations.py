# Author: Morris Zhao
# Date: 2023-01-17

from data import listing_search
from visualizations import plot_mercedes_price
import pandas as pd
import altair as alt
import numpy as np

def test_plot_mercedes_price():
    """
    Tests to ensure all the required are met.
    """
    # Create a small dataframe with one column named 'price' (just for testing).
    df = pd.DataFrame(np.random.randint(10000, 500000, 1000), columns=['price'])
    
    # Test when input model is an integer, the function will throw an error
    try:
        plot_mercedes_price(10, 450000, df)
    except Exception as e:
        # Check if the correct exception was raised
        assert str(e) == "The first input should be a string contain the specific model", f"Unexpected exception raised: {e}"
    else:
        # If no exception was raised, fail the test
        assert False, "Expected exception was not raised"
    
    # Test when input price is a string, the function will throw an error
    try:
        plot_mercedes_price('glb 35', '400000', df)
    except Exception as e:
        # Check if the correct exception was raised
        assert str(e) == "The second input should be a number (the price of the car)", f"Unexpected exception raised: {e}"
    else:
        # If no exception was raised, fail the test
        assert False, "Expected exception was not raised"
        
    # Test when input market_df is a dataframe, the function will throw an error
    try:
        plot_mercedes_price('glb 35', 400000, 1234)
    except Exception as e:
        # Check if the correct exception was raised
        assert str(e) == "The third input should be a pd.DataFrame", f"Unexpected exception raised: {e}"
    else:
        # If no exception was raised, fail the test
        assert False, "Expected exception was not raised"
    
    # Test whether the function returns a plot
    if not isinstance(plot_mercedes_price('glb-35', 450000, df), alt.LayerChart):
        raise Exception("Function did not return an Altair chart")