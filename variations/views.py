from django.core.serializers import json
from django.http import JsonResponse

def my_view(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(json_data)
    return JsonResponse({'status': 'success'})

