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


def chatbot(request):
    if request.method == 'POST':
        question = request.POST['question']
        context = request.POST['context']
        answer = answer_question(question, context)
        return render(request, 'chatbot.html', {'question': question, 'context': context, 'answer': answer})
    else:
        return render(request, 'chatbot.html')
