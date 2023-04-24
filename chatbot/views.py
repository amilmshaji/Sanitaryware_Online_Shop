from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch


def answer_question(question, context):
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
    return answer


from django.http import JsonResponse

def chatbot(request):
    print("working")
    if request.method == 'POST':
        question = request.POST['question']
        context = "Django is a powerful and widely used web framework written in Python that allows developers to build robust web applications quickly and efficiently. It follows the Model-View-Template (MVT) architecture, which promotes clean separation of concerns and encourages reusable code. Django provides a plethora of built-in features and tools that simplify common web development tasks such as URL routing, authentication, database management, and form handling."
        answer = answer_question(question, context)
        print("getting")
        print(answer)
        response_data = {'question': question, 'context': context, 'answer': answer}
        return JsonResponse(response_data)
    else:
        return render(request, 'dash-my-profile.html')

