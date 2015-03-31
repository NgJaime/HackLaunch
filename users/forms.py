from django import forms
from models import Skill, MakerTypes
from zxcvbn_password.fields import PasswordField, PasswordConfirmationField
from django.conf import settings


class UserProfileForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=30, min_length=1)
    last_name = forms.CharField(label='Last name', max_length=30, min_length=1)
    location = forms.CharField(label='Location', max_length=128)
    summary = forms.CharField(label='summary', max_length=256, required=False)
    # todo the skil marker types queries could be cached
    skills = forms.TypedMultipleChoiceField(label='Skills',
                                            coerce=int,
                                            choices=[(skill.id, skill.name) for skill in Skill.objects.all()],
                                            required=False)
    maker_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                           choices=[(maker_type.id, maker_type.name) for maker_type in MakerTypes.objects.all()],
                                           required=False)
    image = forms.ImageField(widget=forms.FileInput)
    password = PasswordField(widget=None)
    password_confirmation = PasswordConfirmationField(widget=None)

    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if 'image' in self.changed_data:
            if image:
                if image._size > settings.MAX_IMAGE_SIZE:
                    raise forms.ValidationError("Max image size 5Mb.")
                return image
            else:
                raise forms.ValidationError("Could not read uploaded image.")

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()

        if 'password' in cleaned_data and 'password_confirmation' not in cleaned_data \
                or 'password' not in cleaned_data and 'password_confirmation' in cleaned_data \
                or ('password' in cleaned_data and 'password_confirmation' in cleaned_data
                    and cleaned_data['password'] != cleaned_data['password_confirmation']):

                raise forms.ValidationError('Passwords do not match')

        return cleaned_data


