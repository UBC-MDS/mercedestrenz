# Author: Ty Andrews
# Date: 2023-01-16

from bs4 import BeautifulSoup
from requests import get
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}


class KijijiScraper:
    def __init__(self):
        self.base_url = "https://www.kijiji.ca"
        self.results_df = pd.DataFrame()

    def scrape_search_results(self, search_result_url: str, limit=100):
        """Appends a single page of search results to the results_df attribute.

        Parameters
        ----------
        search_result_url : str
            The url of the search results page to scrape.
        limit : int, optional
            Max number of results to scrape from the page, by default 100

        Examples
        --------
        >>> scraper = KijijiScraper()
        >>> scraper.scrape_search_results("https://www.kijiji.ca/b-alberta/\
            toyota-rav4/k0l9003?rb=true&dc=true")
        >>> scraper.results_df.head()
        """

        response = get(search_result_url, headers=headers)
        html_soup = BeautifulSoup(response.text, "html.parser")

        # each ad is contained in a div with class "search-item"
        search_results = html_soup.find_all("div", class_="search-item")

        results = []

        for result in search_results[0:limit]:

            # the "data-vip-url" attribute contains the link to the ad details
            ad_url = result["data-vip-url"]
            # the unique identifying listing id
            listing_id = result["data-listing-id"]

            # skip ads that are not for cars or trucks
            if ad_url.split("/")[1] not in ["v-cars-trucks"]:
                print(f"Found ad for {ad_url.split('/')[1]}, skipping.")
                continue

            ad_link = "https://www.kijiji.ca" + ad_url

            ad_dict = self.scrape_ad_page(ad_link, listing_id)

            if ad_dict is not None:
                results.append(ad_dict)
            print("Ad done...")

        # convert the results to a dataframe
        results_df = pd.DataFrame(results)

        self.results_df = pd.concat([self.results_df, results_df])

        self.clean_scraped_results()

    def clean_scraped_results(self):
        """Cleans the scraped results."""

        try:
            self.results_df.mileageFromOdometer = (
                self.results_df.mileageFromOdometer.str.replace("km", "")
                .str.replace(",", "")
                .astype(int, errors="ignore")
            )
        except Exception as e:
            print("Issue with mileageFromOdometer: ", e)
        try:
            self.results_df.vehicleModelDate = self.results_df.vehicleModelDate.astype(
                int, errors="ignore"
            )
        except Exception as e:
            print("Issue with vehicleModelDate: ", e)

    def scrape_ad_page(self, ad_link: str, listing_id: int):
        """Extracts the details from a single ad page.

        Parameters
        ----------
        ad_link : str
            The url of the ad page to scrape.
        listing_id : int
            The unique identifying listing id

        Returns
        -------
        dict
            The details of the ad.
        """

        # get the ad details from it's link
        ad_details = get(ad_link, headers=headers)
        ad_soup = BeautifulSoup(ad_details.content, "html.parser")
        attr_list = ad_soup.find(id="AttributeList")

        # some ad items don't have attributes
        if attr_list is None:
            return None

        ad_dict = {}
        ad_dict["ad_link"] = ad_link
        ad_dict["listing_id"] = listing_id
        ad_dict["date_posted"] = self.get_date_posted(ad_soup)
        ad_dict["price"] = self.get_car_price(ad_soup)
        ad_dict["price_currency"] = self.get_price_currency(ad_soup)
        ad_dict["vehicle_location"] = self.get_vehicle_location(ad_soup)
        for a in attr_list.find_all("dd"):
            try:
                ad_dict[a["itemprop"]] = a.text
            except:
                pass
        ad_dict["description"] = self.get_car_description(ad_soup)

        return ad_dict

    def get_car_description(self, ad_html):
        """Extracts the description from the ad page.

        Parameters
        ----------
        ad_html : BeautifulSoup
            The html of the ad page.

        Returns
        -------
        str
            The description of the vehicle ad.
        """
        try:
            return ad_html.find("div", itemprop="description").text
        except:
            return None

    def get_car_price(self, ad_html):
        """Extracts the price from the ad page.

        Parameters
        ----------
        ad_html : BeautifulSoup
            The html of the ad page.

        Returns
        -------
        float
            The price of the vehicle ad.
        """
        try:
            price_string = ad_html.find("span", itemprop="price").text.strip()
            price = float(price_string.replace("$", "").replace(",", ""))
            return price
        except:
            return None

    def get_price_currency(self, ad_html):
        """Extracts the currency from the ad page.

        Parameters
        ----------
        ad_html : BeautifulSoup
            The html of the ad page.

        Returns
        -------
        str
            The currency of the vehicle ad.
        """
        try:
            return ad_html.find("span", itemprop="priceCurrency")["content"]
        except:
            return None

    def get_date_posted(self, ad_html):
        """Extracts the date the ad was posted from the ad page.

        Parameters
        ----------
        ad_html : BeautifulSoup
            The html of the ad page.

        Returns
        -------
        str
            The date the ad was posted.
        """
        try:
            return ad_html.find("div", itemprop="datePosted")["content"]
        except:
            return None

    def get_vehicle_location(self, ad_html):
        """Extracts the location of the vehicle from the ad page.

        Parameters
        ----------
        ad_html : BeautifulSoup
            The html of the ad page.

        Returns
        -------
        str
            The location of the vehicle.
        """
        try:
            return ad_html.find("span", itemprop="address").text
        except:
            return None
