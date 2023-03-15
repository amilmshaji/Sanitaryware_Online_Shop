from django.contrib import admin

# Register your models here.
from recommendation.models import SearchHistory

admin.site.register(SearchHistory)
