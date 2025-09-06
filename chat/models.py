from django.db import models
import uuid

class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class MessageLog(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message_text = models.TextField()
    direction = models.CharField(max_length=20, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')])
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('sent', 'Sent'), ('delivered', 'Delivered'), ('read', 'Read')], default='sent')

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=500, blank=True)
    last_updated = models.DateTimeField(auto_now=True)