# from django.core.serializers import json
from django.http import JsonResponse
import requests


def my_view(request):
    # if request.method == 'POST':
    #     json_data = json.loads(request.body)
    #     print(json_data)
    # return JsonResponse({'status': 'success'})

    #sending value to fastapi
    # url = "http://localhost:8000/items_add"
    #
    # data = {"id":9 ,"name": "diya","description":"very good", "stock": 10}
    #
    # response = requests.post(url, json=data)
    #
    # item = response.json()
    # print(response)
    #
    # print(item)  # {"name": "example item", "price": 10.0}

    response = requests.get("http://localhost:8000/mydata")
    data1 = response.json()["mydata"]
    print(data1)
    return JsonResponse({'status': 'success'})

