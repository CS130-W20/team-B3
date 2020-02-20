from django.urls import include, path
from rest_framework import routers
from . import views, accountviews, listingviews, sellingviews, swipeviews, paymentviews

router = routers.DefaultRouter()
# Code to register API urls will go here
urlpatterns = [
    path('accounts/create/', accountviews.account_create),
    path('accounts/update/', accountviews.account_update),

    path('selling/sell/', sellingviews.sell_swipe),

    path('swipes/sget/', swipeviews.get_swipes),

    path('pay/ask/'    , paymentviews.make_payment),
    path('pay/confirm/', paymentviews.confirm_payment),
    path('pay/transfer', paymentviews.transfer_to_seller),

]
