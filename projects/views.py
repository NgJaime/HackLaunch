from django.shortcuts import render
from django.views.generic.edit import FormView
from projects.forms import ProjectForm
from base.views import LoginRequiredMixin

def project(request):
    return render(request, 'project.html')


class ProjectEditView(LoginRequiredMixin, FormView):
    form_class = ProjectForm
    template_name = "project_edit.html"
    success_url = '/'


