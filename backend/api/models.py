from django.db import models

# Create your models here.
class Location(models.Model):
	id = models.CharField(max_length=255, primary_key=True)
	lat = models.DecimalField(max_digits=9, decimal_places=6)
	lng = models.DecimalField(max_digits=9, decimal_places=6)

class DiningHall(Location):
	open_at = models.TimeField()
	close_at = models.TimeField()
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=255)
	picture = models.URLField()

class User(models.Model):
	USER_STATES = [
		('0', 'New'),
		('1', 'Active'),
		('2', 'Banned')
	]
	status = models.CharField(max_length=1, choices=USER_STATES)
	id = models.CharField(max_length=255, primary_key=True)
	pp_email = models.EmailField()

class Account(User):
	home_loc = models.OneToOneField(Location, on_delete=models.DO_NOTHING)
	pw = models.CharField(max_length=255)
	phone = models.CharField(max_length=30) #Doesn't make sense to use numerical, we'll need to validate though

class Swipe(models.Model):
	SWIPE_STATES = [
		('0', 'Available'),
		('1', 'Sold'),
		('2', 'Finalized'),
		('3', 'Refunded')
	]
	status = models.CharField(max_length=1, choices=SWIPE_STATES)
	seller = models.OneToOneField(User, on_delete=models.DO_NOTHING)
	location = models.ForeignKey(DiningHall, on_delete=models.DO_NOTHING) #possibly add on_delete=models.CASCADE, but we might want to keep data around
	price = models.DecimalField(max_digits=5, decimal_places=2)

class Bid(models.Model):
	BID_STATES = [
		('0', 'Pending'),
		('1', 'Accepted'),
		('2', 'Rejected')
	]
	status = models.CharField(max_length=1, choices=BID_STATES)
	swipe = models.ForeignKey(Swipe, on_delete=models.CASCADE)
	buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	bid_price = models.DecimalField(max_digits=5, decimal_places=2)

class Transaction(models.Model):
	sender = models.CharField(max_length=255)
	recipient = models.CharField(max_length=255)
	paid = models.DateTimeField()
	total = models.DecimalField(max_digits=5, decimal_places=2)
	details = models.CharField(max_length=255)

class Listing(models.Model):
	swipe = models.ForeignKey(Swipe, on_delete=models.CASCADE)
	seller_loc = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
	description = models.CharField(max_length=300)
	visible_from = models.TimeField()
	visible_to = models.TimeField()