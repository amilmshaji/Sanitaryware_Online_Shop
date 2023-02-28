# from django.core.serializers import json
# from django.core.serializers import json
from django.http import JsonResponse
import requests

from variations.models import Brand_Company


def my_view(request):
    response = requests.get("http://localhost:8080/mydata")
    data1 = response.json()["mydata"]
    print(data1)

    # Append values to Brand table
    for item in data1:
        brand = Brand_Company()
        brand.brand = item.get('name')
        brand.description = item.get('description')
        brand.save()

    return JsonResponse({'status': 'success'})



