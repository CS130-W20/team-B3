from django.urls import include, path
from rest_framework import routers
from . import views, accountviews, sellviews, swipeviews, paymentviews, buyviews

router = routers.DefaultRouter()
# Code to register API urls will go here
urlpatterns = [

    path('', views.default),

    path('accounts/create/', accountviews.account_create),
    path('accounts/check/', accountviews.account_checkexistence),
    path('accounts/update/', accountviews.account_update),
    path('accounts/user_data/', accountviews.account_data),

    path('selling/get_bid/', swipeviews.get_best_pairing, name='get_bid'),
    path('selling/sell/', sellviews.swipe_sellswipe),

    path('buying/get_swipe/', swipeviews.get_best_pairing, name='get_swipe'),
    path('buying/buy/', buyviews.bid_placebid),

    path('swipes/homescreen_info/', swipeviews.get_swipes),
    path('swipes/timeinterval_info/', swipeviews.lowestswipe_highestbid_info),

    path('pay/ask/', paymentviews.make_payment),
    path('pay/confirm/', paymentviews.confirm_payment),
    path('pay/transfer/', paymentviews.transfer_to_seller)
]
