import json
from django import forms
from django.core.urlresolvers import reverse_lazy
from froala_editor.widgets import FroalaEditor
from datetime import datetime
from projects.models import Project
from users.models import Skill


class ProjectForm(forms.ModelForm):
    new_timeline_post = forms.CharField(widget=FroalaEditor(options={'placeholder': 'Create a new post for your project it can include images, videos and embeded youtube content.'}))
    new_timeline_post_title = forms.CharField(widget=FroalaEditor(options={'inlineMode': True,
                                                                           'placeholder': 'Add a title for your new post',
                                                                           'colorGroups': {'text': 'Text', 'cmd': 'foreColor', 'colors': ['#FFFFFF' 'REMOVE']}}))
    date = datetime.now().strftime("%d/%m/%Y")
    month = datetime.now().strftime("%B")

    technologies = json.dumps(list(Skill.objects.values_list('name', flat=True)), ensure_ascii=False).encode('utf8')

    get_user_url = reverse_lazy('get_user')

    class Meta:
        model = Project
        fields = ['tag_line', 'pitch', 'posts', 'title', 'tags', 'creators', 'logo',
                  'facebook', 'google_plus', 'instagram', 'pinterest', 'twitter']
