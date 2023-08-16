from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("listing",views.listing, name = "listing"),
    path("listing_view/<int:item_id>",views.listing_view, name = "listing_view"),
    path("watchlist/<int:item_id>",views.watchlists, name = "watchlist"),
    path("removeWatch", views.removeWatch, name = "removeWatch"),
    path("watchlistView", views.watchlistView, name = "watchlistView"),
    path("Bid/<int:item_id>", views.bid, name = "Bid"),
    path("Categories", views.Categories, name = "Categories"),
    path("categoriesView/<str:item_cat>", views.categoriesView, name = "categoriesView"),
    path("comments/<int:item_id>", views.comments, name = "comments"),
    path("closeBid/<int:item_id>", views.closeBid, name = "closeBid"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
