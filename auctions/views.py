from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing
from .forms import ListingForm


def index(request):
    title = "Active Listings"
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True),
        "title" : title
    })

def all(request):
    title = "All Listings"
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "title" : title
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:       
        return render(request, "auctions/register.html")
    
def newlisting(request):
    if request.method == "POST":
        form1 = ListingForm(request.POST)
        if (form1.is_valid()):
            listing = form1.save(commit=False) #Why? Because we want to set the owner (a field not included in the form) before saving.
            listing.owner = request.user
            listing.current_bid = listing.starting_bid
            listing.save()
            return redirect('index')  ## change this to that listing page afterwards
        #something like
        #  return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
        else:
            return render(request, "auctions/newListing.html", {
                "form1": form1
            })
    
    return render(request, "auctions/newListing.html", {
        "form1": ListingForm()
    })
