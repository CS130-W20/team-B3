from django.urls import include, path
from rest_framework import routers
from . import views, accountviews, sellviews, buyviews, swipeviews

router = routers.DefaultRouter()
# Code to register API urls will go here
urlpatterns = [
    path('accounts/create/', accountviews.account_create),
    path('accounts/update/', accountviews.account_update),
    path('selling/sell/', sellviews.swipe_sellswipe),
    path('swipes/sget/', swipeviews.get_swipes),
	path('bid/place/', buyviews.bid_placebid)
]
