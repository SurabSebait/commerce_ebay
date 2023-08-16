from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to = "auction/images", default="")
    desc = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    name2 = models.CharField(max_length=350)
    close_list = models.CharField(max_length = 3, default = "")

    
    def __str__(self):
        return f"{self.name}"
    
class watchlist(models.Model):
    username = models.CharField(max_length=200)
    name = models.CharField(max_length = 200)

    def __str__(self):
        return f"{self.name}"
    
class Bid(models.Model):
    username = models.CharField(max_length = 200)
    item_name = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return f"Bid by {self.username}"
    
class Comment(models.Model):
    username = models.CharField(max_length=100)
    comment = models.CharField(max_length = 100000)
    item_name = models.CharField(max_length = 30, default = "")

    def __str__(self):
        return f"commented by {self.username}"

    
