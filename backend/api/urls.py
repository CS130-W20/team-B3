from django.urls import include, path
from rest_framework import routers
from . import views, accountviews, listingviews

router = routers.DefaultRouter()
# Code to register API urls will go here
urlpatterns = [
    path('accounts/create/', accountviews.account_create),
    path('accounts/update/', accountviews.account_update),
    path('listings/create/', listingviews.listing_create),
    path('listings/bid/place/', listingviews.listing_placebid),
    path('listings/bid/update/', listingviews.listing_updatebid),
    path('listings/bid/bget/', listingviews.buyergetbids)
]
