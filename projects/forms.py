from django import forms
from django.forms.models import inlineformset_factory
from django.forms.formsets import BaseFormSet
from projects.models import Project, Post


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['tag_line', 'pitch', 'title', 'logo',
                  'facebook', 'google_plus', 'instagram', 'pinterest', 'twitter']


class PostForm(forms.ModelForm):
    # class Meta:
    #     model = Post
    #     fields = '__all__'

    def clean_author(self):
        pass

    def clean(self):
        pass

    def clean_title(self):
        pass

class BasePostFormSet(BaseFormSet):
    def clean(self):
        for form in self.forms:
            form.empty_permitted = False

ProjectPostSet = inlineformset_factory(Project, Post, formset=BasePostFormSet, fields='__all__', extra=1)
