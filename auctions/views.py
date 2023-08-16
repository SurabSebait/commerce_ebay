from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    menu = Listing.objects.all()

    return render(request, "auctions/index.html",{"lists":menu})


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
    
@login_required
def listing(request):
    if request.method == "POST":
        username = request.user.username
        print(username)
        product_name = request.POST["product_name"]
        product_img = request.POST["product_img"]
        product_details = request.POST["product_details"]
        start_bid = request.POST["starting_bid"]
        product_category = request.POST["product_category"]
        b = Listing(name2 = username,name = product_name, image= product_img, desc = product_details, price = start_bid, category = product_category)
        b.save()
        params = { "name":product_name, "image":product_img, "bid":start_bid,"username":username, "category":product_category, "details":product_details}
        return render(request, "auctions/listing_page.html",params)
        
    else:
        return render(request, "auctions/listing.html")

@login_required  
def listing_view(request, item_id):
    item = Listing.objects.get(pk = item_id) 
    current_user = request.user.username 
    bidder = Bid.objects.filter(item_name = item)
    comments = Comment.objects.filter(item_name = item.name)
    if item.close_list != '':
        for prod in bidder:
            if prod.item_name == item.name and prod.price == item.price:
                message = item.close_list
                name = prod.username
                if name == current_user:
                    params = {"list":item, "bidder":bidder, "current_user":current_user, "name": name}
                    return render(request, "auctions/listing_view.html",params)
                else:
                    params = {"list":item, "bidder":bidder, "current_user":current_user,"message": message}
                    return render(request, "auctions/listing_view.html",params)
                
    elif item.close_list == '':
        list1 = []
        for comment in comments:
            s = f"commented by {comment.username}: {comment.comment}"
            list1.append(s)
        print(list1)
        params = {"list":item, "bidder":bidder, "current_user":current_user, "list1":list1}
        return render(request, "auctions/listing_view.html",params)
    

@login_required
def watchlistView(request):
    username = request.user.username
    watch_item = watchlist.objects.filter(username = username)
    prod = Listing.objects.all()
    items = []

    for x in watch_item:
        for y in prod:
            if x.name == y.name:
                items.append(y)

    params = {"items":items}
    return render(request, "auctions/watchlist_view.html", params)

    
@login_required
def watchlists(request, item_id):
    item = Listing.objects.get(pk = item_id)
    current_user = request.user.username
    products = watchlist.objects.all()
    if current_user != item.name2:
        count = 0
        for i in range(len(products)):
            if products[i].name == item.name and products[i].username == current_user:
                count += 1

        if count == 0:
            b = watchlist(username = current_user, name = item.name)
            b.save()

        products1 = watchlist.objects.all()
        listn = []
        for i in range(len(products1)):
            if products1[i].username == current_user:
                listn.append(products1[i].name)

        
        return HttpResponseRedirect(reverse("watchlistView"))
    else:
        return render(request, "auctions/watchlist.html", {"message":"You can't add your own listing"})

@login_required
def bid(request, item_id):
    if  request.method == "POST":
        biding = int(request.POST["bid"])
        item = Listing.objects.get(pk = item_id)
        bidder = request.user.username
        if bidder != item.name2:
            if biding > item.price:
                b = Bid(username = bidder, item_name = item.name, price = biding)
                b.save()
                Listing.objects.filter(pk=item_id).update(price=biding)
                return HttpResponseRedirect(reverse("listing_view", args = (item_id, )))
            else:
                return render(request, "auctions/error.html", {"message":"Error\nBid more than the minimum price"})
            
@login_required
def closeBid(request, item_id):
    Listing.objects.filter(pk=item_id).update(close_list = "The item is delisted.")
    return HttpResponseRedirect(reverse("listing_view", args = (item_id, )))

@login_required
def comments(request, item_id):
    if request.method == "POST":
        comments = request.POST["comment"]
        username1 = request.user.username
        item = Listing.objects.get(pk = item_id) 
        b = Comment(username = username1, comment = comments, item_name = item.name)
        b.save()
        return HttpResponseRedirect(reverse("listing_view", args = (item_id, )))
    


@login_required
def Categories(request):
    items = Listing.objects.all()
    lists = []
    l1 = set(lists)
    for item in items:
        l1.add(item.category)
    params = {"items": l1}
    return render(request, "auctions/category.html", params)


@login_required
def categoriesView(request, item_cat):
    items = Listing.objects.filter(category = item_cat)
    params = {"items":items, "cat_name":item_cat}
    return render(request, "auctions/categoriesView.html",params)


def removeWatch(request):
    username = request.user.username
    if request.method == 'POST':
        item = Listing.objects.get(pk = int(request.POST["items"]))
        instance = watchlist.objects.filter(username = username, name = item.name)
        instance.delete()
        return HttpResponseRedirect(reverse("watchlistView"))