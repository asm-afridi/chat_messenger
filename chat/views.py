from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import facebook
import json
from django.conf import settings
from django.http import HttpResponse
from .models import User, MessageLog
import google.generativeai as genai

class MessengerWebhookView(APIView):
    def get(self, request):
        # Handle webhook verification
        verify_token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        print(f"Verify Token: {verify_token}, Challenge: {challenge}")
        if verify_token == settings.FB_VERIFY_TOKEN:
            return HttpResponse(challenge, content_type='text/plain')
        return Response({'error': 'Invalid verify token'}, status=status.HTTP_403_FORBIDDEN)

    def generate_ai_response(self, message_text, user_id):
        """Generate AI response using Google Gemini"""
        try:
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Get conversation history for context
            recent_messages = MessageLog.objects.filter(user_id__user_id=user_id).order_by('-timestamp')[:5]
            context = []
            for msg in reversed(recent_messages):
                role = "User" if msg.direction == "incoming" else "Assistant"
                context.append(f"{role}: {msg.message_text}")
            
            # Build conversation context
            conversation_history = "\n".join(context) if context else ""
            
            # Create prompt with context
            prompt = f"""You are a helpful and friendly chatbot assistant. Keep responses conversational and under 200 characters for messaging.

Conversation history:
{conversation_history}

User: {message_text}

Please respond naturally and helpfully:"""
            
            # Generate response
            response = model.generate_content(prompt)
            
            return response.text.strip()
            
        except Exception as e:
            print(f"AI response generation failed: {e}")
            return f"I received your message: '{message_text}'. How can I help you?"

    def post(self, request):
        # Handle incoming messages
        data = request.data
        if data.get('object') == 'page':
            for entry in data.get('entry', []):
                for event in entry.get('messaging', []):
                    sender_id = event['sender']['id']
                    if 'message' in event:
                        message_text = event['message'].get('text')
                        # Log message to database
                        user, created = User.objects.get_or_create(user_id=sender_id, defaults={'name': 'Unknown'})
                        MessageLog.objects.create(
                            user_id=user,
                            message_text=message_text,
                            direction='incoming'
                        )
                        # Send AI-generated response
                        try:
                            ai_response = self.generate_ai_response(message_text, sender_id)
                            self.send_message(sender_id, ai_response)
                        except Exception as e:
                            print(f"Failed to send AI reply to {sender_id}: {e}")
                            # Continue processing without crashing
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    def send_message(self, recipient_id, message_text):
        # Send message via Facebook Graph API
        print(f"Attempting to send message to {recipient_id}: {message_text}")
        
        token = settings.FB_PAGE_ACCESS_TOKEN
        print(f"Using token: {token[:20] if token else 'None'}...")
        
        if not token:
            raise Exception("FB_PAGE_ACCESS_TOKEN is not set or is None")
        
        # Use requests instead of facebook-sdk for better control
        import requests
        url = f"https://graph.facebook.com/v19.0/me/messages"
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            'recipient': {'id': recipient_id},
            'message': {'text': message_text},
            'messaging_type': 'RESPONSE'
        }
        
        params = {'access_token': token}
        
        try:
            response = requests.post(url, headers=headers, json=payload, params=params)
            result = response.json()
            print(f"Facebook API response: {result}")
            
            if response.status_code != 200:
                print(f"Facebook API error: {result}")
                raise Exception(f"Facebook API error: {result}")
            
            # Log outgoing message only if successful
            user, created = User.objects.get_or_create(user_id=recipient_id, defaults={'name': 'Unknown'})
            MessageLog.objects.create(
                user_id=user,
                message_text=message_text,
                direction='outgoing',
                status='sent'
            )
        except Exception as e:
            print(f"Error sending message: {e}")
            print(f"Error type: {type(e)}")
            raise e

# --- API endpoint to send message manually ---
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def send_message_api(request):
    """
    POST /chat/send_message/
    Body: {"recipient_id": "<PSID>", "message_text": "Hello!"}
    """
    recipient_id = request.data.get('recipient_id')
    message_text = request.data.get('message_text')
    
    if not recipient_id or not message_text:
        return Response({'error': 'recipient_id and message_text required'}, status=400)
    
    # Use the MessengerWebhookView send_message method
    webhook_view = MessengerWebhookView()
    try:
        webhook_view.send_message(recipient_id, message_text)
        return Response({'status': 'sent'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)