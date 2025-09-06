# Facebook Messenger Chatbot with Django REST API & Gemini AI

A Django REST Framework-based Facebook Messenger chatbot that uses Google Gemini AI to provide intelligent, context-aware responses to users.

## 🚀 Features

- **Facebook Messenger Integration**: Webhook endpoints for receiving and sending messages
- **AI-Powered Responses**: Google Gemini AI generates intelligent, contextual replies
- **Conversation History**: Maintains context with the last 5 messages per user
- **Message Logging**: Stores all incoming and outgoing messages in database
- **REST API**: Manual message sending endpoint for testing and automation
- **Error Handling**: Graceful fallbacks when AI or messaging fails
- **Environment Variables**: Secure configuration management

## 🛠️ Tech Stack

- **Backend**: Django 5.2.5 + Django REST Framework
- **Database**: SQLite (default, easily configurable)
- **AI**: Google Gemini 1.5-flash
- **Messaging**: Facebook Messenger Platform API
- **Environment**: Python 3.12+ with virtual environment

## 📋 Prerequisites

- Python 3.12+
- Facebook Developer Account
- Facebook Page
- Google AI Studio Account (for Gemini API)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/asm-afridi/chat_messenger.git
   cd chat_messenger
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework requests google-generativeai python-dotenv
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Django Core Settings
   SECRET_KEY=your-django-secret-key-here
   DEBUG=True
   
   # Facebook Messenger Bot Environment Variables
   FB_VERIFY_TOKEN=your-webhook-verify-token
   FB_PAGE_ACCESS_TOKEN=your-page-access-token
   
   # Google Gemini API Key for GenAI responses
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver 0.0.0.0:6000
   ```

## 🔑 API Keys Setup

### Facebook Setup

1. **Create Facebook App**: Go to [Facebook Developers](https://developers.facebook.com/)
2. **Add Messenger Product**: Configure webhook and get page access token
3. **Set Webhook URL**: `https://your-domain.com/api/webhook/`
4. **Verify Token**: Use any string as `FB_VERIFY_TOKEN`

### Google Gemini Setup

1. **Visit Google AI Studio**: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. **Create API Key**: Generate and copy your Gemini API key
3. **Add to .env**: Set `GEMINI_API_KEY=your-actual-key`

## 🌐 API Endpoints

### Webhook Endpoint
- **GET** `/api/webhook/` - Facebook webhook verification
- **POST** `/api/webhook/` - Receive messages from Facebook

### Manual Messaging
- **POST** `/api/send_message/` - Send messages manually

**Request Body:**
```json
{
  "recipient_id": "facebook-user-psid",
  "message_text": "Your message here"
}
```

**Response:**
```json
{
  "status": "sent"
}
```

## 🗄️ Database Schema

### Models

- **User**: Stores Facebook user information
  - `user_id` (Primary Key): Facebook PSID
  - `name`: User display name
  - `created_at`: Registration timestamp

- **MessageLog**: Conversation history
  - `message_id`: Unique message identifier
  - `user_id`: Foreign key to User
  - `message_text`: Message content
  - `direction`: incoming/outgoing
  - `timestamp`: Message timestamp
  - `status`: sent/delivered/read

## 🤖 AI Response System

The chatbot uses Google Gemini to generate intelligent responses:

1. **Context Building**: Retrieves last 5 messages for conversation context
2. **AI Generation**: Sends context to Gemini with system prompts
3. **Response Formatting**: Keeps responses under 200 characters for messaging
4. **Fallback**: Provides helpful fallback if AI fails

## 🚀 Deployment

### Environment Variables for Production

```env
SECRET_KEY=production-secret-key
DEBUG=False
FB_VERIFY_TOKEN=your-verify-token
FB_PAGE_ACCESS_TOKEN=your-page-token
GEMINI_API_KEY=your-gemini-key
```

### Using Docker (Optional)

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🧪 Testing

### Test Manual Messaging
```bash
curl -X POST http://localhost:6000/api/send_message/ \
  -H "Content-Type: application/json" \
  -d '{"recipient_id": "user-psid", "message_text": "Hello!"}'
```

### Test Webhook
Facebook will automatically test your webhook URL during setup.

## 📂 Project Structure

```
chat_messenger/
├── chat/                      # Main app
│   ├── models.py             # User and MessageLog models
│   ├── views.py              # Webhook and API views
│   ├── urls.py               # App URL routing
│   └── migrations/           # Database migrations
├── messenger_api/            # Django project
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI application
├── .env                      # Environment variables
├── .gitignore               # Git ignore rules
├── manage.py                # Django management
└── README.md                # This file
```

## 🔍 Troubleshooting

### Common Issues

1. **Webhook Verification Failed**
   - Check `FB_VERIFY_TOKEN` matches Facebook app settings
   - Ensure webhook URL is accessible from internet

2. **AI Responses Not Working**
   - Verify `GEMINI_API_KEY` is valid
   - Check Google AI Studio quota/billing

3. **Messages Not Sending**
   - Confirm `FB_PAGE_ACCESS_TOKEN` is correct
   - Verify Facebook page permissions

4. **Database Errors**
   - Run migrations: `python manage.py migrate`
   - Check database permissions

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **ASM Afridi** - [asm-afridi](https://github.com/asm-afridi)

## 🙏 Acknowledgments

- Django REST Framework team
- Facebook Messenger Platform
- Google Gemini AI
- Open source community

## 📞 Support

For support, email your-email@example.com or create an issue in the repository.

---

**⭐ If you found this project helpful, please give it a star!**
