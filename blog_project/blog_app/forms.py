from django import forms
from .models import User, Blog, Comment, Like

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=128, widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', "username", 'email', 'phone', 'profession', 'password']

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs= { 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={ 'class': 'form-control'}),
            'phone': forms.TextInput(attrs ={'class': 'form-control'}),
            'profession': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs= { 'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords does not match!")
        


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=128,widget=forms.PasswordInput(attrs={'class':'form-control'}))


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body', 'feature_image']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs= { 'class': 'form-control', 'id':"editor1"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content':forms.TextInput(attrs={'class':'form-control'})
        }
    


     

