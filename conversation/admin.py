from django.contrib import admin

# Register your models here.

from .models import ConversationMessage, Conversation

admin.site.register(ConversationMessage)
admin.site.register(Conversation)
