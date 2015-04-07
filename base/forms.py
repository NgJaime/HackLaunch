from django import forms
from django.contrib.auth import authenticate
from zxcvbn_password.fields import PasswordField


class InitialPassword(forms.Form):
    email = forms.EmailField(label="email", required=True, max_length=255)
    password = PasswordField(widget=None)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        if not user or not user.is_active:
                raise forms.ValidationError("An account for " + email +
                                            " already exists but your password was invalid")

        return self.cleaned_data
