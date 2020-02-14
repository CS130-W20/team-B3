from django.db import models

# Create your models here.
class Location(models.Model):
	id = models.CharField(primary_key=True)
	lat = models.DecimalField()
	lng = models.DecimalField()

class DiningHall(Location):
	open_at = models.TimeField()
	close_at = models.TimeField()
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	picture = models.URLField()

class User(models.Model):
	USER_STATES = [
		('0', 'New'),
		('1', 'Active'),
		('2', 'Banned')
	]
	status = models.CharField(max_length=1, choices=USER_STATES)
	id = models.CharField(primary_key=True)
	pp_email = models.EmailField()

class Account(User):
	home_loc = models.OneToOneField(Location)
	pw = models.CharField()
	phone = models.CharField() #Doesn't make sense to use numerical, we'll need to validate though

class Swipe(models.Model):
	SWIPE_STATES = [
		('0', 'Available'),
		('1', 'Sold'),
		('2', 'Finalized'),
		('3', 'Refunded')
	]
	status = models.CharField(max_length=1, choices=SWIPE_STATES)
	seller = models.OneToOneField(User)
	location = models.ForeignKey(DiningHall) #possibly add on_delete=models.CASCADE, but we might want to keep data around
	price = models.DecimalField(decimal_places=2)

class Bid(models.Model):
	BID_STATES = [
		('0', 'Pending'),
		('1', 'Accepted'),
		('2', 'Rejected')
	]
	status = models.CharField(max_length=1, choices=BID_STATES)
	swipe = models.ForeignKey(Swipe)
	buyer = models.ForeignKey(User)
	bid_price = models.DecimalField(decimal_places=2)

class Transaction(models.Model):
	from = models.CharField()
	to = models.CharField()
	paid = models.DateTimeField()
	total = models.DecimalField(decimal_places=2)
	details = model.CharField()

class Listing(models.Model):
	swipe = models.ForeignKey(Swipe)
	seller_loc = models.ForeignKey(Location)
	description = models.CharField(max_length=300)