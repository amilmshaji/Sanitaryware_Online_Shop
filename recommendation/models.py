from django.db import models

# Create your models here.
from django.db import models

from accounts.models import Account


class SearchHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    query = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.query)
