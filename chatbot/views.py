from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch


def answer_question(question, context):
    user_input = question.lower().strip()
    if user_input == "hi" or user_input == "hello" or user_input == "hlo":
        answer= "Hello! How can I assist you today?"
    else:
        tokenizer = AutoTokenizer.from_pretrained('squirro/albert-base-v2-squad_v2')
        model = AutoModelForQuestionAnswering.from_pretrained('squirro/albert-base-v2-squad_v2')
        inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]
        outputs = model(**inputs)
        answer_start_scores = outputs.start_logits
        answer_end_scores = outputs.end_logits
        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    if answer == "[CLS]":
        answer = "sorry i cannot find the result. Can you specify with the context"

    return answer


from django.http import JsonResponse

def chatbot(request):
    print("working")
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

