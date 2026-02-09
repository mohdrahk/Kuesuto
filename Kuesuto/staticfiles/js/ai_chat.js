// Toggle chat window open/close
function toggleChat() {
  const chatWindow = document.getElementById('chat-window');
  const chatBubble = document.getElementById('chat-bubble');

  if (chatWindow.classList.contains('visible')) {
    // Close
    chatWindow.classList.remove('visible');
    chatWindow.classList.add('hidden');
    chatBubble.classList.remove('hidden');
    chatBubble.classList.add('visible');
  } else {
    // Open
    chatWindow.classList.remove('hidden');
    chatWindow.classList.add('visible');
    chatBubble.classList.remove('visible');
    chatBubble.classList.add('hidden');
  }
}

// Get CSRF token for Django security
function getCookie(name) {
  let cookieValue = null;

  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();

      if (cookie.substring(0, name.length + 1) === `${name}=`) {
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
  chatMessages.innerHTML += `<div class="ai-msg" id="loading"><span>Thinking...</span></div>`;
  chatMessages.scrollTop = chatMessages.scrollHeight;

  try {
    const response = await fetch('/ai/ask/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ question })
    });

    const data = await response.json();
    document.getElementById('loading')?.remove();

    if (data.success) {
      chatMessages.innerHTML += `<div class="ai-msg"><span>${data.answer}</span></div>`;
    } else {
      chatMessages.innerHTML += `<div class="ai-msg"><span>Error: ${data.error}</span></div>`;
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
  } catch (error) {
    document.getElementById('loading')?.remove();
    chatMessages.innerHTML += `<div class="ai-msg"><span>Connection error! Please try again.</span></div>`;
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

// Handle Enter key press
document.addEventListener('DOMContentLoaded', () => {
  const chatInput = document.getElementById('chat-input');

  if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendChatMessage();
      }
    });
  }
});
