import google.generativeai as genai
from django.conf import settings
import json


class GeminiAIService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def answer_question(self, question, user_data):
        prompt = f"""
You are a helpful AI study assistant for KUESUTO.
You MUST adhere to these rules:
1. Only use information found from Student Info listed below.
2. You can respond to greetings normally but If the user asks a question that cannot be answered using ONLY the provided context, you MUST respond with a specific, canned rejection message.
3. You are explicitly forbidden from answering general knowledge questions, discussing topics outside the context, or engaging in casual conversation.

Rejection message to use:
"I am sorry, but I can only answer questions related to Kuesuto . I cannot answer that question."


Student Info:
- Username: {user_data.get('username')}
- Score: {user_data.get('score', 0)}
- Active Plans: {user_data.get('active_plans', 0)}
- Active Tasks: {user_data.get('active_tasks', 0)}
- Completed Tasks: {user_data.get('completed_tasks', 0)}

Their Plans: {user_data.get('plans', [])}


Question: {question}
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Sorry, error: {str(e)}"
