from djongo import models


class Location(models.Model):
    """
    Location object. Various locations are stored in this table, including those for dining halls, home locations of
    users, and (later) current locations of sellers
    """
    loc_id = models.AutoField(primary_key=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)


class DiningHall(Location):
    """
    DiningHall object. Used as filtering criteria for buyers and sellers to specify where they want to use / sell
    their Swipes at. Inherits from Location.
    """

    hall_id = models.AutoField(primary_key=True)
    hours = models.ListField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    picture = models.URLField()


class User(models.Model):
    """
    User object. Both buyers and sellers are users.
    """
    USER_STATES = [
        ('0', 'New'),
        ('1', 'Active'),
        ('2', 'Banned')
    ]
    status = models.CharField(max_length=1, choices=USER_STATES, default=0)
    user_id = models.CharField(max_length=255, primary_key=True)
    pp_email = models.EmailField()


class Account(User):
    """
    Account object. Each user has an account. Inherits from User.
    """
    home_loc = models.OneToOneField(Location, on_delete=models.DO_NOTHING)
    # Frontend hashes the password, alternatively we can use Django authentication
    pw = models.CharField(max_length=255)
    # Doesn't make sense to use numerical, we'll need to validate on the front-end though
    phone = models.CharField(max_length=30)


class Swipe(models.Model):
    """
    Swipe object. The commodity.
    """
    SWIPE_STATES = [
        ('0', 'Available'),
        ('1', 'Sold'),
        ('2', 'Finalized'),
        ('3', 'Refunded')
    ]
    swipe_id = models.AutoField(primary_key=True)
    # Gets set to 1 after a buyer/seller pairing has occured, 2 when the buyer/seller meet up and confirm, 3 if the seller didn't have the swipe and a refund needs to happen
    status = models.CharField(max_length=1, choices=SWIPE_STATES, default=0)
    seller = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # References user_id of the seller in question
    location = models.ForeignKey(DiningHall, on_delete=models.DO_NOTHING)  # References hall_id of DiningHall
    price = models.DecimalField(max_digits=5, decimal_places=2)
    visibility = models.ListField()  # An array of JSON objects that contains intervals when this listing should appear on the app


class Bid(models.Model):
    """
    Bid object. The criteria a buyer specifies for a swipe such that he/she is willing to purchase the swipe.
    """
    BID_STATES = [
        ('0', 'Pending'),  # Doesn't meet minimum, sits in the queue until an eligible listing pops up
        ('1', 'Accepted'),  # Pairing between buyer and seller has been made (either at the time of bid or after a swipe was created)
        ('2', 'Confirmed'),  # Transaction has occured between buyer and seller, whether successful or refund-based
    ]
    bid_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=1, choices=BID_STATES, default=0)
    swipe = models.ForeignKey(Swipe, on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    location = models.ForeignKey(DiningHall, on_delete=models.DO_NOTHING)
    bid_price = models.DecimalField(max_digits=5, decimal_places=2)
    desired_time = models.TimeField(null=True)


class Transaction(models.Model):
    """
    Transaction object. Represents the agreement between seller and buyer for exchanging money for a swipe.
    """
    t_id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    paid = models.DateTimeField()
    total = models.DecimalField(max_digits=5, decimal_places=2)
    details = models.CharField(max_length=255)
