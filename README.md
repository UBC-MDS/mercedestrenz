# mercedestrenz

This python package is for inspecting and analyzing used Mercedes Benz car prices. The package helps users to get simple answers on how to choose the used Mercedes Benz car in the market. The package also includes useful visualization tool and trained model to serve buyers and sellers.

## Collaborators

Kelly Wu, Morris Zhao, Spencer Gerlach, Ty Andrews

## Python ecosystem

Our package is unique, it provides an easy way to investigate used Mercedes Benz car prices. It provide people a big picture about the market. The package relies on a real market data set to plot, filter and predict. It also gives advice to buyers and sellers when they try to make a decision.

## Functions

The package contains the following functions:
1. `load_sample_mercedes_listings`: Retrieves a data frame that contains sample data of used Mercedez Benz vehicles.
2. `plot_mercedes_price`: Plot a density plot of a Mercedes-Benz model to see where the current vehicle's price falls for that same model in the market.
3. `listing_search`: Retrieves the top listings that are within the budget range specified by the user.
4. `predict_mercedes_price`: Predicts the price in USD of a Mercedes-Benz given the year, model, odometer reading, condition and paint color.

## Package dataset

The package contains a static dataset for Craiglist used-car listings that were previously web scraped. Several key attributes about the used-car are available in the dataset, such as vehicle prices, models, car conditions, odometer readings, VINs, regions and transmission. The package's dataset was adapted from verison 10 of the raw dataset created by [AustinReese](https://github.com/AustinReese/UsedVehicleSearch).

## Installation

```bash
$ pip install mercedestrenz
```

## Usage

Below is a basic example of how to use each of the four functions included in this package.

```
# Load all required package functions
from mercedestrenz.data import load_sample_mercedes_listings, listing_search
from mercedestrenz.modelling import train_mercedes_price_prediction_model
from mercedestrenz.modelling import predict_mercedes_price

# Load the sample mercedes listings data into a dataframe
data = load_sample_mercedes_listings()

# Return the top listings that are within a budget range specified by the user. Returns a pandas dataframe of results.
listing_search(data, budget=[2000, 20000], model = "any", sort_feature = "odometer_mi", ascending = True)

# Plot a price distribution of specific mercedes models, and see where an input price falls in the distribution.
plot_mercedes_price(model='s-class', price=80000, market_df=data))

# Predict the price (in USD) of a Mercedes-Benz given the year, model, condition, paint color, and odometer reading.
predict_mercedes_price("e-class", 2015, 55_000, "fair", "silver")
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`mercedestrenz` was created by Kelly Wu, Morris Zhao, Spencer Gerlach, Ty Andrews. It is licensed under the terms of the MIT license.

## Credits

`mercedestrenz` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
