from django import forms 
from .models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        #fields='__all__'
        exclude=['add_task']

class CommentForm(forms.ModelForm):
    class Meta:
         model=Comment
         fields=['name','email','body']      