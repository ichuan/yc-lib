from django import forms
from ycdjbbs.bbs.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('subject', 'content', )

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', )
