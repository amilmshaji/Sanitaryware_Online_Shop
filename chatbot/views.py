import webbrowser

import requests
from django.shortcuts import render
API_URL = "https://api-inference.huggingface.co/models/squirro/albert-base-v2-squad_v2"
headers = {"Authorization": "Bearer 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"}


def answer_question(question, context):
    pages = ["home","map","category", "shop", "login","logout", "register","myprofile"]
    user_input = question.lower().strip()
    if user_input == "hi" or user_input == "hello" or user_input == "hlo":
        answer= "Hello! How can I assist you today?"
    elif user_input in pages:
        link = f'http://127.0.0.1:8000/{user_input}'
        answer = f"Sure, I can help you navigate to the {user_input} page. <a href='{link}' style='color:red;'>Click Here</a>"
        webbrowser.open_new_tab(link)

    elif user_input == "help" or user_input == "hellp" or user_input == "hellp me" or user_input == "help me":
        answer= "I can help you navigate to different pages on our website. Just tell me which page you'd like to visit, or type 'menu' to see a list of options."
    elif user_input == "menu":
        answer= "Here are some options:\nhome,\nmap,\ncategory\n,shop\n,login,\nregister,\nlogout"
    else:

        payload = {
            "inputs": {
                "question": question,
                "context": context
            }
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        answer = response.json()['answer']
    print(answer)
    if answer == "[CLS]" or answer =='':
        answer = "sorry i cannot find the result. Can you specify with the context"

    return answer



from django.http import JsonResponse

def chatbot(request):
    if request.method == 'POST':
        question = request.POST['question']

        context = '''Sanitaryware Online Store platform is an online marketplace that specializes in selling sanitaryware
         products. The platform offers a wide range of products, including toilets, wash basins, mirrors, bathtubs, 
        shower mixers'''

        answer = answer_question(question, context)
        print(answer)
        response_data = {'question': question, 'context': context, 'answer': answer}
        return JsonResponse(response_data)
    else:
        return render(request, 'chatbot.html')

