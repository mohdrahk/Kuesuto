// Toggle chat window open/close
function toggleChat() {
  const chatWindow = document.getElementById('chat-window');
  const chatBubble = document.getElementById('chat-bubble');

  if (chatWindow.style.display === 'none') {
    chatWindow.style.display = 'flex';
    chatBubble.style.display = 'none';
  } else {
    chatWindow.style.display = 'none';
    chatBubble.style.display = 'block';
  }
}

// Get CSRF token for Django security
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Send message to AI
async function sendChatMessage() {
  const input = document.getElementById('chat-input');
  const question = input.value.trim();

  if (!question) return;

  // Show user message
  const chatMessages = document.getElementById('chat-messages');
  chatMessages.innerHTML += `<div class="user-msg"><span>${question}</span></div>`;
  input.value = '';

  // Show loading
  chatMessages.innerHTML += `<div class="ai-msg" id="loading"><span>...</span></div>`;
  chatMessages.scrollTop = chatMessages.scrollHeight;

  try {
    const response = await fetch('/ai/ask/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ question: question })
    });

    const data = await response.json();
    document.getElementById('loading').remove();

    if (data.success) {
      chatMessages.innerHTML += `<div class="ai-msg"><span>${data.answer}</span></div>`;
    } else {
      chatMessages.innerHTML += `<div class="ai-msg"><span>Error: ${data.error}</span></div>`;
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
  } catch (error) {
    document.getElementById('loading').remove();
    chatMessages.innerHTML += `<div class="ai-msg"><span>Connection error!</span></div>`;
  }
}

// Handle Enter key press
document.addEventListener('DOMContentLoaded', function() {
  const chatInput = document.getElementById('chat-input');
  if (chatInput) {
    chatInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        sendChatMessage();
      }
    });
  }
});
