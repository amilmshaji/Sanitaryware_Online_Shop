import webbrowser
from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import requests
from django.shortcuts import render
from django.template.defaultfilters import safe

tokenizer = AutoTokenizer.from_pretrained('squirro/albert-base-v2-squad_v2')
model = AutoModelForQuestionAnswering.from_pretrained('squirro/albert-base-v2-squad_v2')
from shop_app.models import Product

# API_URL = "https://api-inference.huggingface.co/models/squirro/albert-base-v2-squad_v2"
# headers = {"Authorization": "Bearer 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"}


def answer_question(question, context):
    pages = ["home","cart","category", "store", "login","logout", "register","myprofile"]
    user_input = question.lower().strip()
    if user_input == "hi" or user_input == "hello" or user_input == "hlo":
        answer= "Hello! How can I assist you today?"
    elif user_input in pages:
        link = f'http://127.0.0.1:8000/{user_input}'
        answer = f"Sure, I can help you navigate to the {user_input} page. <a href='{link}' style='color:red;'>Click Here</a>"
        # webbrowser.open_new_tab(link)

    elif user_input == "help" or user_input == "hellp" or user_input == "hellp me" or user_input == "help me":
        answer= "I can help you navigate to different pages on our website. Just tell me which page you'd like to visit, or type 'menu' to see a list of options."
    elif user_input == "menu":
        answer= f'Here are some options:\n1home\n2.category\n3.store\n4.login\n5.register\n6.logout\n7.cart\n8.orders\n9.myprofile'
    else:

        # payload = {
        #     "inputs": {
        #         "question": question,
        #         "context": context
        #     }
        # }
        # response = requests.post(API_URL, headers=headers, json=payload)
        # answer = response.json()['answer']
        # print(response.json())

        inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]
        outputs = model(**inputs)
        answer_start_scores = outputs.start_logits
        answer_end_scores = outputs.end_logits
        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    print(answer)
    if answer == "[CLS]" or answer =='':
        answer = "sorry i cannot find the result. Can you specify with the context"
    word_to_remove="[CLS]"
    word_to_remove1="[SEP]"

    if word_to_remove in answer:
        answer = answer.replace(word_to_remove, "")

    if word_to_remove1 in answer:
        answer = answer.replace(word_to_remove1, "")
    if question in answer:
        answer = answer.replace(question, "")


    return answer
from django.http import JsonResponse
def chatbot(request):
    details = " "
    product_list = []
    for product in Product.objects.all():
        details += " " + str(product.product_name) + ","
        product_list.append(details)
    if request.method == 'POST':
        question = request.POST['question']
        context = f'''
        {details}  
        Sanitaryware Online Store platform is an online marketplace that specializes in selling sanitaryware
         products. '''
        answer = answer_question(question, context)
        print(answer)
        response_data = {'question': question, 'context': context, 'answer': safe(answer)}
        return JsonResponse(response_data)
    else:
        return render(request, 'chatbot.html')

