import json
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django_ajax.decorators import ajax
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from datetime import datetime
from users.models import Skill
from projects.forms import ProjectForm, ProjectCreatorsForm
from base.views import LoginRequiredMixin

from projects.models import Project, ProjectCreators, Technologies, ProjectTechnologies, Tags, ProjectTags


class ProjectView(TemplateView):
    template_name = 'project.html'


# class ProjectEditView(LoginRequiredMixin, FormView):
#     form_class = ProjectForm
#     template_name = "project_edit.html"
#     success_url = '/'
#
#     def get_initial(self):
#         initial = super(ProjectEditView, self).get_initial()
#
#         # todo get or crate
#         self.project, created = Project.objects.get_or_create(id=5)
#
#         initial['creators'] = self.project.projectcreators_set.all()
#         initial['title'] = self.project.title
#         initial['pitch'] = self.project.pitch
#
#         return initial

#
# class ProjectCreateView(CreateView):
#     template_name = 'project_edit.html'
#     model = Project
#     form_class = ProjectForm
#     success_url = '/'
#
#     def get(self, request, *args, **kwargs):
#         """
#         Handles GET requests and instantiates blank versions of the form
#         and its inline formsets.
#         """
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#
#         project = get_object_or_404(Project, id=5)
#         project_creators = project.projectcreators_set.all()
#
#         creator_form = CreatorsFormSet(instance=project)
#         return self.render_to_response(self.get_context_data(form=form, creator_form=creator_form))
#
#     def post(self, request, *args, **kwargs):
#         """
#         Handles POST requests, instantiating a form instance and its inline
#         formsets with the passed POST variables and then checking them for
#         validity.
#         """
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#
#         creator_form = CreatorsFormSet(self.request.POST)
#         if (form.is_valid() and creator_form.is_valid()):
#             return self.form_valid(form, creator_form)
#         else:
#             return self.form_invalid(form, creator_form)
#
#     def form_valid(self, form, creator_form):
#         """
#         Called if all forms are valid. Creates a Recipe instance along with
#         associated Ingredients and Instructions and then redirects to a
#         success page.
#         """
#         self.object = form.save()
#         creator_form.instance = self.object
#         creator_form.save()
#         return HttpResponseRedirect(self.get_success_url())
#
#     def form_invalid(self, form, creator_form):
#         """
#         Called if a form is invalid. Re-renders the context data with the
#         data-filled forms and errors.
#         """
#         return self.render_to_response(
#             self.get_context_data(form=form, creator_form=creator_form))


def get_project_context(project_id):
    date = datetime.now().strftime("%d/%m/%Y")
    month = datetime.now().strftime("%B")
    # todo cache
    technologies = json.dumps(list(Skill.objects.values_list('name', flat=True)), ensure_ascii=False).encode('utf8')
    context = {'date': date, 'month': month, 'technologies': technologies, 'projectId': project_id}

    return context


@csrf_protect
def projectCreate(request):
    if request.method == "GET":
        new_project = Project.objects.create()
        new_creators = ProjectCreators.objects.create(project=new_project, creator=request.user, is_admin=True)

        project_form = ProjectForm(instance=new_project)

        context = get_project_context(new_project.id)

        return render_to_response('project_edit.html',
                                  {'project_form': project_form,
                                   'project_creators': new_project.projectcreators_set.all(),
                                   'context': context}, RequestContext(request))
    else:
        return Http404()


@csrf_protect
def projectEdit(request):
    if request.method == "POST":
        project_form = ProjectForm(request.POST)

        if project_form.is_valid():
            project_form.save()

        render_to_response('home.html')

        # project_form = ProjectForm(request.POST, instance=ProjectForm())
        # project_creators = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range(0,3)]
        #
        # if pform.is_valid() and all([cf.is_valid() for cf in cforms]):
        #     new_poll = pform.save()
        #     for cf in cforms:
        #         new_choice = cf.save(commit=False)
        #         new_choice.poll = new_poll
        #         new_choice.save()
        #     return HttpResponseRedirect('/polls/add/')
    else:
        current_project = get_object_or_404(Project, id=5)
        project_form = ProjectForm(instance=current_project)

        context = get_project_context(current_project.id)

        return render_to_response('project_edit.html',
                                  {'project_form': project_form,
                                   'project_creators': current_project.projectcreators_set.all(),
                                   'project_technologies': current_project.projecttechnologies_set.all(),
                                   'context': context},
                                  RequestContext(request))


@ajax
@csrf_protect
def addCreator(request):
    if request.method == "POST":
        # In your view that is processing the form request
        if request.is_ajax():
            form = ProjectCreatorsForm(request.POST)

            if form.is_valid():
                goal = form.save()
                return {'result': '888'}
                # Serialize the goal in json format and send the
                # newly created object back in the reponse
                # data = serializers.serialize('json', [goal,])

            # else:
            #     # Since form.errors is a proxy need to create a dict from it with unicode
            #     data = json.dumps(dict([(k, [unicode(e) for e in v]) for k,v in form.errors.items()]))
            # return HttpResponse(data, mimetype='application/json')

            return {'result': '8881'}


@ajax
@csrf_protect
def add_technology(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST and 'technology' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    creator = project.projectcreators_set.get(creator_id=request.user.id)

                    if creator.is_admin:
                        technology, created = Technologies.objects.get_or_create(name=request.POST['technology'])
                        ProjectTechnologies.objects.create(project=project, technology=technology)
                        return {'success': True}
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}
                except IntegrityError:
                    return {'success': False, 'message': 'Technology already assigned to project'}

    return {'success': False, 'message': 'Invalid request'}

