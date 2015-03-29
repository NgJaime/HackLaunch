from django import forms
from models import Skill
from zxcvbn_password.fields import PasswordField, PasswordConfirmationField


class UserProfileForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=30, min_length=1)
    last_name = forms.CharField(label='Last name', max_length=30, min_length=1)
    location = forms.CharField(label='Location', max_length=128)
    summary = forms.CharField(label='summary', max_length=256, required=False)
    skills = forms.TypedMultipleChoiceField(label='Skills',
                                            coerce=int,
                                            choices=[(skill.pk, skill.name) for skill in Skill.objects.all()],
                                            required=False)
    image = forms.ImageField()
    password = PasswordField(widget=None)
    password_confirmation = PasswordConfirmationField(widget=None)

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()

        if 'password' in cleaned_data and 'password_confirmation' not in cleaned_data \
                or 'password' not in cleaned_data and 'password_confirmation' in cleaned_data \
                or ('password' in cleaned_data and 'password_confirmation' in cleaned_data
                    and cleaned_data['password'] != cleaned_data['password_confirmation']):

                raise forms.ValidationError('Passwords do not match')

        return cleaned_data


