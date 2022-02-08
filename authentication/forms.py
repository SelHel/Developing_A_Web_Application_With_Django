from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'placeholder': "Nom d'utilisateur",
            'maxlength': '16',
            'minlength': '5',
            })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password',
            'id': 'password',
            'type': 'password',
            'placeholder': 'Mot de passe',
            'maxlength': '22',
            'minlength': '8'
            })

    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'placeholder': "Nom d'utilisateur",
            'maxlength': '16',
            'minlength': '5',
            })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password1',
            'id': 'password1',
            'type': 'password',
            'placeholder': 'Mot de passe',
            'maxlength': '22',
            'minlength': '8'
            })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password2',
            'id': 'password2',
            'type': 'password',
            'placeholder': 'Confirmez mot de passe',
            'maxlength': '22',
            'minlength': '8'
            })

    username = forms.CharField(max_length=20, label=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2']
