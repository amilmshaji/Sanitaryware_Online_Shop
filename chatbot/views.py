from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import random

# Define a function to handle user input and generate a response
def get_response(user_input):
    pages = ["home", "about", "products", "services", "contact"]
    user_input = user_input.lower().strip()
    if user_input == "hi" or user_input == "hello":
        return "Hello! How can I assist you today?"
    elif user_input in pages:
        return f"Sure, I can help you navigate to the {user_input} page. Here's the link: www.example.com/{user_input}"
    elif "help" in user_input:
        return "I can help you navigate to different pages on our website. Just tell me which page you'd like to visit, or type 'menu' to see a list of options."
    elif user_input == "menu":
        return "Here are some options:\nHome\nAbout\nProducts\nServices\nContact"
    else:
        return "I'm sorry, I didn't understand. Please try again or type 'help' for assistance."

# Define a function to handle the chatbot
def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST['user_input']
        response = get_response(user_input)
        return render(request, 'chatbot.html', {'response': response})
    else:
        return render(request, 'chatbot.html')
