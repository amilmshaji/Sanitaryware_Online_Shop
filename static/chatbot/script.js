const chatForm = document.getElementById('chat-form');
const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');

chatForm.addEventListener('submit', sendMessage);

function sendMessage(e) {
	e.preventDefault();
	const message = messageInput.value;
	if (message.trim() === '') {
		return false;
	}
	appendMessage(message, 'user');
	getAnswer(message);
	messageInput.value = '';
}

function getAnswer(message) {
  const url = `/chatbot?question=${encodeURIComponent(message)}`;
  fetch(url)
    .then(response => response.json())
    .then(data => appendMessage(data.answer, 'bot'))
    .catch(error => console.log(error));
}

