from django.db import models

# Create your models here.


class userDetails(models.Model):
    firstName = models.CharField(max_length=25)
    lastName = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = "userDetails"

