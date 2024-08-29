from django.forms import ModelForm
from django import forms
from .models import *

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Add message ...', 'class': 'p-4 text-black', 'maxlength':'300', 'autofocus': True}),
        }

class NewGroupForm(ModelForm):
    class Meta: 
        model = ChatGroup
        fields = ['groupchat_name']
        widget = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Add message ...', 'class': 'p-4 text-black', 'maxlength':'300', 'autofocus': True,
            }),
        }