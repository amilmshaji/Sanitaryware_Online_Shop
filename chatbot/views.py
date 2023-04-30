import requests
from django.shortcuts import render

API_URL = "https://api-inference.huggingface.co/models/squirro/albert-base-v2-squad_v2"
headers = {"Authorization": "Bearer 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"}


def answer_question(question, context):
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    answer = response.json()['answer']
    return answer


from django.http import JsonResponse

def chatbot(request):
    print("working")
    if request.method == 'POST':
        question = request.POST['question']
        context = "Django is a powerful and widely used web framework written in Python that allows developers to build robust web applications quickly and efficiently. It follows the Model-View-Template (MVT) architecture, which promotes clean separation of concerns and encourages reusable code. Django provides a plethora a of built-in features and tools that simplify common web development tasks such as URL routing, authentication, database management, and form handling."
        answer = answer_question(question, context)
        print("getting")
        print(answer)
        response_data = {'question': question, 'context': context, 'answer': answer}
        return JsonResponse(response_data)
    else:
        return render(request, 'chatbot.html')

