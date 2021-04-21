from django import forms
from .models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password',
                          widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)',
                        widget=forms.PasswordInput())

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self._errors['password2'] = self.error_class(['Password mismatched'])
        
        return self.cleaned_data.get('password2')

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        exclude = ['id','user']
        widgets = {
            'body' : forms.Textarea(attrs={
                'maxlength': '5000',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)