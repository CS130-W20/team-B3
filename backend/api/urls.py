from django.urls import include, path
from rest_framework import routers
from . import views, accountviews

router = routers.DefaultRouter()
#Code to register API urls will go here
urlpatterns = [
	path('accounts/create/', accountviews.account_create),
	path('accounts/update/', accountviews.account_update)
]