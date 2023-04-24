from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.forms.models import model_to_dict

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            context['message'] = "Successful LOGIN."
            return render(request, 'djangoapp/index.html', context)
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    logout(request)
    context['message'] = "Successful LOGOUT. BYE."
    return render(request, 'djangoapp/index.html', context)

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/efdde710-d7aa-41ae-8ef8-627df2a6a5bc/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)
        # return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/efdde710-d7aa-41ae-8ef8-627df2a6a5bc/api/reviews?dealerId=" + str(dealer_id)
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["reviews"] = reviews
        # Concat all dealer's short name
        # reviews_list  = []
        # reviews_list.append([review.review for review in reviews])
        # Return a list of dealer short name
        # return HttpResponse(reviews_list)
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):

    context = {}

    if request.user.is_authenticated:
        print("***user is authent.")
    

    if request.method == 'GET':

        return redirect('djangoapp/add_review', dealer_id=dealer_id)

    elif request.method == 'POST':

        url1 = "https://us-south.functions.appdomain.cloud/api/v1/web/efdde710-d7aa-41ae-8ef8-627df2a6a5bc/api/reviews?dealerId=" + str(dealer_id)
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url1, dealer_id)
        context["reviews"] = reviews

        data =  reviews[0]
        data.review = "This is a great car dealer"
        json_payload = json.dumps(data.__dict__)


        url = "https://us-south.functions.appdomain.cloud/api/v1/web/efdde710-d7aa-41ae-8ef8-627df2a6a5bc/api/review"
        # Get dealers from the URL
        reviews = post_request(url, json_payload)
        # Concat all dealer's short name
        print("***")
        print(reviews)
        reviews_list  = []
        reviews_list.append([review.review.review for review in reviews])
        # Return a list of dealer short name
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

