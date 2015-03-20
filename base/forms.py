from django import forms
from zxcvbn_password.fields import PasswordField


class InitialPassword(forms.Form):
    email = forms.EmailField(label="email", required=True, max_length=255)
    password = PasswordField(widget=None)

    def clean(self):
        # todo
        print 'in the clean function '

