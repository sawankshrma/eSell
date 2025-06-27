from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watched_by") #remember


class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('FN', 'Fashion'),
        ('TY', 'Toys'),
        ('EL', 'Electronics'),
        ('HM', 'Home'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='HM')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')

    def __str__(self):
        return f"{self.title} from user: ({self.owner.username})"


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} from user: ({self.user.username}) @ {self.listing.title}"


class Comment(models.Model):
    text = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"
