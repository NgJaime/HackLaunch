import json
from django import forms
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse_lazy
from froala_editor.widgets import FroalaEditor
from datetime import datetime
from projects.models import Project, ProjectCreators
from users.models import Skill


class ProjectForm(forms.ModelForm):
    new_timeline_post = forms.CharField(widget=FroalaEditor(options={'placeholder': 'Create a new post for your project it can include images, videos and embeded youtube content.'}),
                                        required=False)
    new_timeline_post_title = forms.CharField(widget=FroalaEditor(options={'inlineMode': True,
                                                                           'placeholder': 'Add a title for your new post',
                                                                           'colorGroups': {'text': 'Text', 'cmd': 'foreColor', 'colors': ['#FFFFFF' 'REMOVE']}}),
                                              required=False)

    class Meta:
        model = Project
        fields = ['tag_line', 'pitch', 'posts', 'title', 'tags', 'logo',
                  'facebook', 'google_plus', 'instagram', 'pinterest', 'twitter', 'id']


class ProjectCreatorsForm(forms.ModelForm):
    class Meta:
        model = ProjectCreators
        fields = ['project', 'creator', 'date_joined', 'summary']

CreatorsFormSet = inlineformset_factory(Project, ProjectCreators, fields=['project', 'creator', 'date_joined', 'summary'], extra=5)
