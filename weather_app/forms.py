from django import forms
from weather_app.models import Comment

class commentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text']
        labels = {'name': 'Your name', 'text': 'Your comment'}