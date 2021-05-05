"""CSC111 Winter 2021 Course Project: API Manager

Authors: Michele Massa, Nischal Nair, Nathan Zavys-Cox

Description: This module contains the functions to return data to be used in the program. It also
contains a function that makes requests to the Skyscanner Flight Search API to fetch data about
the prices of flights between 2 countries.

This file is copyright (c) 2021 Michele Massa, Nischal Nair and Nathan Zavys-Cox."""
import csv
import json
import requests

from algorithm_classes_v2 import WeightedGraph
from randomdata import get_countries_to_codes, get_saved_prices


def make_price_request(origin_code: str, destination_code: str) -> int:
    """ Given 2 country codes, returns the current min price of a flight between the countries.
    Price is given in CAD. If nothing is returned by the api, the function returns -1
    """
    url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices" \
          f"/browsequotes/v1.0/{origin_code}/CAD/en-US/{origin_code}/{destination_code}/anytime"
    querystring = {"inboundpartialdate": "anytime"}
    headers = {
        'x-rapidapi-key': "090fba85ffmsh85e95425e452236p1d8c76jsnf7cdd2e7fd50",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_response = json.loads(response.text)
    # check if there actually are any quotes
    if "Quotes" in json_response and len(json_response["Quotes"]) > 0:
        return json.loads(response.text)["Quotes"][0]["MinPrice"]
    else:
        return -1


def get_new_prices_from_api() -> dict:
    """ Gets all of the edges for the required weighted graph by making api calls using the csv
    file. Note this function will take around 50 seconds to run since there are many http requests
    being made.

    # Uncomment this test to test how the api works (gets new values)
    # >>> get_new_prices_from_api()
    """
    edges = {}
    countries_to_codes = get_countries_to_codes()
    with open('datasets/country_edges.csv') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            edges[(row[0], row[1])] = make_price_request(countries_to_codes[row[0]],
                                                         countries_to_codes[row[1]])
    return edges


def world_countries_graph(width: int, height: int, fetch_new_data: bool = False) -> WeightedGraph:
    """ Returns a world map graph where the vertices are countries and edges are the cost to fly
    from one country to the other. If fetch_new_data then the function will make api calls the
    get updated flight data. If not the function will use presaged flight data to be faster.
    """
    menu_positions = [(x, y) for y in range(0, height) for x in range(0, width)]

    g = WeightedGraph()

    if fetch_new_data:
        edge_data = get_new_prices_from_api()
    else:
        edge_data = get_saved_prices()
    with open('datasets/countries.csv') as csv_file:
        reader = csv.reader(csv_file)
        i = 0
        for row in reader:
            pos = menu_positions[i]
            g.add_vertex((float(row[1]), float(row[2])), row[0], pos)
            i += 1

    with open('datasets/country_edges.csv') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            country1_pos = [v for v in g.vertices if g.vertices[v].name == row[0]][0]
            country2_pos = [v for v in g.vertices if g.vertices[v].name == row[1]][0]
            price = edge_data[(row[0], row[1])]
            # check to make sure the price is valid before adding the edge
            # since if no prices are returned for the flight the price will be -1
            if price > 0:
                g.add_edge(country1_pos, country2_pos, price)
    return g


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E9999', 'E9998', 'R0913', 'R0902'],
        'extra-imports': [],
        'max-nested-blocks': 5
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()
