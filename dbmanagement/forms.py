from django import forms

class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password=forms.CharField(widget=forms.PasswordInput)

class SearchForm(forms.Form):
    search_text = forms.CharField(widget=forms.TextInput)