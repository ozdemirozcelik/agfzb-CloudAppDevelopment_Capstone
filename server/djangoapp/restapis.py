import requests, os
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import random


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))

    # params["text"] = kwargs["text"]
    # params["version"] = kwargs["version"]
    # params["features"] = kwargs["features"]
    # params["return_analyzed_text"] = kwargs["return_analyzed_text"]

    try:
        # print("***")
        # if kwargs["api_key"]:
        #     # Basic authentication GET
        #     response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
        # else:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data

    except:
        # If any error occurs
        print("***Network exception occurred")


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def post_request(url, data):
    print("POST to {} ".format(url))

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data

    except:
        # If any error occurs
        print("***Network exception occurred")

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        # For each review object
        for review in json_result:
            # Get its content in `doc` object
            # Create a DealerReview object
            review_obj = DealerReview(_id = review["_id"], _rev= review["_rev"], purchase=review["purchase"], review=review["review"], purchase_date=review["purchase_date"],
                                   car_make=review["car_make"], car_model=review["car_model"], car_year=review["car_year"],
                                   id=review["id"], name=review["name"], sentiment="neutral", dealership=review["dealership"])
            sentiment_list = ["positive","positive","positive","positive","neutral","neutral","negative"]
            review_obj.sentiment = random.choice(sentiment_list)
            # review_obj = DealerReview(purchase=review["purchase"], review=review["review"], purchase_date=review["purchase_date"],
            #                        car_make=review["car_make"], car_model=review["car_model"], car_year=review["car_year"],
            #                        id=review["id"], name=review["name"])
            results.append(review_obj)

    return results












# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):

    # Get environment variables
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/dabaa507-af4d-4cdf-9bb4-c044b6d313a7"
    # url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/dabaa507-af4d-4cdf-9bb4-c044b6d313a7/v1/analyze?version=2019-07-12"
    api_key = os.environ.get('API_KEY')
    # version = "2019-07-12"


    params = dict()
    print(api_key)
    params["api_key"] = api_key
    params["text"] = text
    # params["version"] = kwargs["version"]
    # params["features"] = kwargs["features"]
    # params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    response = get_request(url, params)

    if response:
        print(response)


