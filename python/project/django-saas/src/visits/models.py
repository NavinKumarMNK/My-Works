from django.db import models


# Create your models here.
class PageVisit(models.Model):
    # db -> table
    # id -> primary key -> autofield -> 1, 2, 3
    path = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
