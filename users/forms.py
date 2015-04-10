import logging
from django import forms
from models import Skill, MakerTypes
from zxcvbn_password.fields import PasswordField, PasswordConfirmationField
from django.conf import settings
from users.models import User

logger = logging.getLogger(__name__)


class UserProfileForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=30, min_length=1)
    last_name = forms.CharField(label='Last name', max_length=30, min_length=1)
    location = forms.CharField(label='Location', max_length=128)
    summary = forms.CharField(label='summary', max_length=256, required=False, widget=forms.Textarea)
    # todo the skil marker types queries could be cached
    skills = forms.TypedMultipleChoiceField(label='Skills',
                                            coerce=int,
                                            choices=[(skill.id, skill.name) for skill in Skill.objects.all()],
                                            required=False)
    maker_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                           choices=[(maker_type.id, maker_type.name) for maker_type in MakerTypes.objects.all()],
                                           required=False)
    image = forms.ImageField(widget=forms.FileInput, required=False)
    password = PasswordField(widget=None, required=False)
    password_confirmation = PasswordConfirmationField(widget=None, required=False)
    username = forms.CharField(label='Username', max_length=30, min_length=1)

    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if 'image' in self.changed_data:
            if image:
                if image._size > settings.MAX_IMAGE_SIZE:
                    raise forms.ValidationError("Max image size 5Mb.")
                return image
            else:
                raise forms.ValidationError("Could not read uploaded image.")

    def clean_username(self):
        username = self.cleaned_data.get('username', False)

        if 'username' in self.changed_data:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # this username does not exist yet
                pass
            except User.MultipleObjectsReturned:
                logger.error("Multiple user for username: " + username)
                pass
            else:
                raise forms.ValidationError("The username " + username + " is not available.")

        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', False)

        if 'first_name' in self.changed_data:
            new_first_name = first_name.title()
            return new_first_name

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', False)

        if 'last_name' in self.changed_data:
            new_last_name = last_name.title()
            return new_last_name

        return last_name

    def clean_location(self):
        location = self.cleaned_data.get('location', False)

        if 'location' in self.changed_data:
            new_location = location.title()
            return new_location

        return location

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()

        if 'password' in cleaned_data and 'password_confirmation' not in cleaned_data \
                or 'password' not in cleaned_data and 'password_confirmation' in cleaned_data \
                or ('password' in cleaned_data and 'password_confirmation' in cleaned_data
                    and cleaned_data['password'] != cleaned_data['password_confirmation']):

                raise forms.ValidationError('Passwords do not match')

        return cleaned_data


