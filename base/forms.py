import logging
from django import forms
from users.models import User
from zxcvbn_password.fields import PasswordField

logger = logging.getLogger(__name__)


class InitialPassword(forms.Form):
    email = forms.EmailField(label="email", required=True, max_length=255)
    password = PasswordField(widget=None)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # this user does not exist yet
            pass
        except User.MultipleObjectsReturned:
            logger.error("Multiple user for email: " + email)
            pass
        else:
            if not user.check_password(password):
                raise forms.ValidationError("An account for " + email + " already exists but your password was invalid")

        return self.cleaned_data
