from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse



from .models import User, Listing
from .forms import ListingForm, BiddingForm, CommentForm


def is_in_watchlist(user, product):
    return product in user.watchlist.all()


def index(request):
    title = "Active Listings"
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True),
        "title" : title
    })

def categories(request):
    return render(request, "auctions/categories.html")

def categories_show(request, id):
    
    category_dict = dict(Listing.CATEGORY_CHOICES)
    title = category_dict.get(id, "Unknown Category")

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=id),
        "title": title
    })


def all(request):
    title = "All Listings"
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "title" : title
    })

@login_required
def liked(request):
    title = "My WatchList"
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(watched_by=request.user),
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
            # return redirect('index')  ## change this to that listing page afterwards
        #something like
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/newListing.html", {
                "form1": form1
            })
    
    return render(request, "auctions/newListing.html", {
        "form1": ListingForm()
    })

@login_required
def bid(request, product_id):
    if request.method == "POST":
        form2 = BiddingForm(request.POST)
        if (form2.is_valid()):
            bidding = form2.save(commit=False) 
            try:
                product = Listing.objects.get(id=product_id)
            except Listing.DoesNotExist:
                raise Http404("Product not found.")
            if bidding.amount < product.current_bid:
                bidding.listing = product
                form2.add_error('amount', "Bid must be greater than the current bid.")
                product = bidding.listing

                

                return render(request, "auctions/product.html", {
                    "listing": product,
                    "comments": product.comments.all(),
                    "bids": product.bids.all(),
                    "form2": form2,
                    "form3" : CommentForm(),
                    "added" : is_in_watchlist(request.user, product)
                })
            #Why? Because we want to set the owner (a field not included in the form) before saving.
            bidding.user = request.user
            bidding.listing = product = get_object_or_404(Listing, id=product_id)
            bidding.save()
            
            # Update current bid
            product.current_bid = bidding.amount
            product.save()

            return HttpResponseRedirect(reverse("product", kwargs={"product_id": product_id}))
        else:
            return render(request, "auctions/product.html", {
                "listing": product,
                "comments": product.comments.all(),
                "bids": product.bids.all(),
                "form2": form2,
                "form3" : CommentForm(),
                "added" : is_in_watchlist(request.user, product)
            })

    try:
        product = Listing.objects.get(id=product_id)
    except Listing.DoesNotExist:
        raise Http404("Product not found.")
    return render(request, "auctions/product.html", {
        "listing": product,
        "comments": product.comments.all(),
        "bids": product.bids.all(),
        "form2": BiddingForm(),
        "form3" : CommentForm(),
        "added" : is_in_watchlist(request.user, product)

    })

@login_required
def comment(request, product_id):
    if request.method == "POST":
        form3 = CommentForm(request.POST)
        try:
            product = Listing.objects.get(id=product_id)
        except Listing.DoesNotExist:
            raise Http404("Product not found.")            
        if (form3.is_valid()):
            comment = form3.save(commit=False) #Why? Because we want to set the owner (a field not included in the form) before saving.
            comment.user = request.user
            
            comment.listing = product
            comment.save()
            return HttpResponseRedirect(reverse("product", kwargs={"product_id": product_id}))
        else:
            return render(request, "auctions/product.html", {
                "listing": product,
                "comments": product.comments.all(),
                "bids": product.bids.all(),
                "form2": BiddingForm(),
                "form3" : form3,
                "added" : is_in_watchlist(request.user, product)
            })
    
    try:
        product = Listing.objects.get(id=product_id)
    except Listing.DoesNotExist:
        raise Http404("Product not found.")
    return render(request, "auctions/product.html", {
        "listing": product,
        "comments": product.comments.all(),
        "bids": product.bids.all(),
        "form2": BiddingForm(),
        "form3" : CommentForm(),
        "added" : is_in_watchlist(request.user, product)

    })


def product(request, product_id):
    try:
        product = Listing.objects.get(id=product_id)
    except Listing.DoesNotExist:
        raise Http404("Product not found.")
    
    context = {
    "listing": product,
    "comments": product.comments.all(),
    "bids": product.bids.all(),
    "form2": BiddingForm(),
    "form3": CommentForm(),
}
    if request.user.is_authenticated:
        context["added"] = is_in_watchlist(request.user, product)

    return render(request, "auctions/product.html", context)


@login_required
def sell(request, product_id):
    try:
        product = Listing.objects.get(id=product_id)
    except Listing.DoesNotExist:
        raise Http404("Product not found.")
    product.is_active = False
    product.save()
    return render(request, "auctions/product.html", {
        "listing": product,
        "comments": product.comments.all(),
        "bids": product.bids.all(),
        "form2": BiddingForm(),
        "form3" : CommentForm(),
        "added" : is_in_watchlist(request.user, product)
    })

@login_required
def like(request, product_id):
    try:
        product = Listing.objects.get(id=product_id)
    except Listing.DoesNotExist:
        raise Http404("Product not found.")
    
    if is_in_watchlist(request.user, product):
        request.user.watchlist.remove(product)
    else:
        request.user.watchlist.add(product)

    # No need to manually save user or product for M2M changes.


    return render(request, "auctions/product.html", {
        "listing": product,
        "comments": product.comments.all(),
        "bids": product.bids.all(),
        "form2": BiddingForm(),
        "form3" : CommentForm(),
        "added" : is_in_watchlist(request.user, product)
    })

