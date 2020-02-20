from djongo import models

# Create your models here.


class Location(models.Model):
    loc_id = models.AutoField(primary_key=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)


class DiningHall(Location):
    hall_id = models.AutoField(primary_key=True)
    hours = models.ListField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    picture = models.URLField()


class User(models.Model):
    USER_STATES = [
        ('0', 'New'),
        ('1', 'Active'),
        ('2', 'Banned')
    ]
    status = models.CharField(max_length=1, choices=USER_STATES, default=0)
    user_id = models.CharField(max_length=255, primary_key=True)
    pp_email = models.EmailField()


class Account(User):
    home_loc = models.OneToOneField(Location, on_delete=models.DO_NOTHING)
    pw = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)  # Doesn't make sense to use numerical, we'll need to validate though


class Swipe(models.Model):
    SWIPE_STATES = [
        ('0', 'Available'),
        ('1', 'Sold'),
        ('2', 'Finalized'),
        ('3', 'Refunded')
    ]
    swipe_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=1, choices=SWIPE_STATES, default=0)
    seller = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    location = models.ForeignKey(DiningHall, on_delete=models.DO_NOTHING)
  # possibly add on_delete=models.CASCADE, but we might want to keep data around
    price = models.DecimalField(max_digits=5, decimal_places=2)
    visibility = models.ListField()


class Bid(models.Model):
    BID_STATES = [
        ('0', 'Pending'),  # Doesn't meet minimum, needs to be approved by the seller
        ('1', 'Accepted'),  # Meets minimum, auto-accepted but seller still hasn't confirmed they can provide it
        ('2', 'Confirmed'),  # Approved by seller
    ]
    bid_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=1, choices=BID_STATES, default=0)
    swipe = models.ForeignKey(Swipe, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    bid_price = models.DecimalField(max_digits=5, decimal_places=2)


class Transaction(models.Model):
    t_id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    paid = models.DateTimeField()
    total = models.DecimalField(max_digits=5, decimal_places=2)
    details = models.CharField(max_length=255)
