from django import forms
from blogs import models


class UserModelForm(forms.ModelForm):
    class Meta():
        model = models.User
        fields =('username','email','password')


class UserProfileModelForm(forms.ModelForm):
    class Meta():
        model =models.UserProfile
        exclude = ('user',)


class PostModelForm(forms.ModelForm):
    class Meta() :
        model = models.Post
        fields = ('author','Title','Text',)


class CommentModelForm(forms.ModelForm):
    class Meta():
        model = models.Comment
        fields = ('Author','Text',)





        
        
