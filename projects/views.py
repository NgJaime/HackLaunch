import json
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.template import RequestContext
from django_ajax.decorators import ajax
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse


from datetime import datetime
from projects.forms import ProjectForm, ProjectPostSet
from base.views import LoginRequiredMixin

from projects.models import Project, ProjectCreator, Technologies, ProjectTechnologies, Tags, Post, ProjectImage, Follower
from users.models import User, Skill


class ProjectTestView(TemplateView):
    template_name = 'project.html'

class ProjectView(DetailView):
    template_name = 'project_view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['creators'] = self.object.projectcreator_set.all()
        context['technologies'] = self.object.projecttechnologies_set.all()
        context['posts'] = self.object.post_set.all()
        return context

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
#         project = get_object_or_404(Project, id=59)
#         project_creators = project.projectcreator_set.all()
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
        new_creators = ProjectCreator.objects.create(project=new_project, creator=request.user, is_admin=True)

        project_form = ProjectForm(instance=new_project)

        context = get_project_context(new_project.id)

        return render_to_response('project_edit.html',
                                  {'project_form': project_form,
                                   'project_creators': new_project.projectcreator_set.all(),
                                   'context': context}, RequestContext(request))
    else:
        return Http404()


class ProjectUpdateView(FormView):
    form_class = ProjectForm
    model = Project
    template_name = 'project_update.html'
    success_url = '/'
    object = None
    project = None

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['project_post_set'] = ProjectPostSet(self.request.POST)
        else:
            context['date'] = datetime.now().strftime("%d/%m/%Y")
            context['month'] = datetime.now().strftime("%B")
            # todo cache
            context['technologies'] = json.dumps(list(Skill.objects.values_list('name', flat=True)), ensure_ascii=False).encode('utf8')
            context['project_id'] = 5
            context['project_creators'] = ProjectCreator.objects.select_related().filter(project_id=59).order_by('date_joined')
            context['project_technologies'] = self.project.projecttechnologies_set.all()
            context['project_tags'] = json.dumps(list(self.project.tags.values_list('name', flat=True)), ensure_ascii=False).encode('utf8')
            context['project_post_set'] = ProjectPostSet(initial=Post.objects.filter(project_id=59).order_by('-date_added').values())
        return context

    def get_initial(self):
        initial = super(ProjectUpdateView, self).get_initial()

        self.project = get_object_or_404(Project, id=59)

        initial['tag_line'] = self.project.tag_line
        initial['pitch'] = self.project.pitch
        initial['title'] = self.project.title
        initial['logo'] = self.project.logo
        initial['facebook'] = self.project.facebook
        initial['google_plus'] = self.project.google_plus
        initial['instagram'] = self.project.instagram
        initial['pinterest'] = self.project.pinterest
        initial['twitter'] = self.project.twitter

        return initial


    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            project = form.save()

            project_post_formset = ProjectPostSet(request.POST)

            if project_post_formset.is_valid():
                for form in project_post_formset:
                    if form.has_changed():
                        form.save()

            return self.form_valid(form, project_post_formset)

        # todo should this return formset?
        return self.form_invalid(form)

    # def form_valid(self, form):
    #     # context = self.get_context_data()
    #     # project_post_set = context['project_post_set']
    #     #
    #     # if project_post_set.is_valid():
    #     #     self.object = form.save()
    #     #     project_post_set.instance = self.object
    #     #     project_post_set.save()
    #     #     return redirect(self.object.get_absolute_url())
    #     # else:
    #     #     return self.render_to_response(self.get_context_data(form=form))
    #     #
    #     # form.save()
    #     # return HttpResponseRedirect("/")
    #
    #     project_updated = False
    #
    #     for change in form.changed_data:
    #         setattr(self.project, change, form.cleaned_data[change])
    #         project_updated = True
    #
    #     if project_updated:
    #         self.project.save()
    #
    #     formset = ProjectPostSet(self.request.POST, instance=self.projectt)
    #     formset.save()

    def form_invalid(self, form):
        return super(ProjectUpdateView, self).form_invalid(form)

@csrf_protect
def projectEdit(request):
    if request.method == "GET":
        # todo check for object below
        # todo check ownership
        current_project = get_object_or_404(Project, id=59)
        # project_form = ProjectForm(instance=current_project)

        context = get_project_context(current_project.id)

        creators = ProjectCreator.objects.select_related().filter(project_id=59).order_by('date_joined')
        # creators = current_project.projectcreator_set.values()
        posts = Post.objects.filter(project=current_project).order_by('-date_added')

        return render_to_response('project_edit.html',
                                  {'project': current_project,
                                   'project_creators': creators,
                                   'project_posts': posts,
                                   'project_technologies': current_project.projecttechnologies_set.all(),
                                   'project_tags': json.dumps(list(current_project.tags.values_list('name', flat=True)), ensure_ascii=False).encode('utf8'),
                                   'context': context},
                                  RequestContext(request))

@ajax
@csrf_protect
def project_ajax_request(function):
    def wrapper(request, *args, **kwargs):
        if request.method == "POST":
            if request.is_ajax():
                if 'project' in request.POST:
                    try:
                        project = Project.objects.get(id=request.POST['project'])
                        request_user = project.projectcreator_set.get(creator_id=request.user.id)

                        if request_user.is_admin:
                            function(request, project, request_user, args, kwargs)
                        else:
                            return {'success': False, 'message':  'Only admins can make an update to a project'}

                    except ObjectDoesNotExist:
                        return {'success': False, 'message': 'Object does not exist'}
                    except IntegrityError:
                        return {'success': False, 'message': 'User already assigned to project'}

@ajax
@csrf_protect
def update_project(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    request_user = project.projectcreator_set.get(creator_id=request.user.id)

                    if request_user.is_admin:
                        updated = False

                        if 'data' in request.POST:
                            data = json.loads(request.POST['data'])

                            if 'field' in data:
                                field = data['field']

                                if field == 'pitch' and 'body' in request.POST:
                                    project.pitch = request.POST['body']
                                    updated = True
                                elif field == 'tagline' and 'body' in request.POST:
                                    project.tag_line = request.POST['body']
                                    updated = True
                                elif field == 'title' and 'body' in request.POST:
                                    project.title = request.POST['body']
                                    updated = True
                                elif 'value' in request.POST['data']:
                                    if field == 'facebook':
                                        project.facebook = data['value']
                                        updated = True
                                    elif field == 'google-plus':
                                        project.google_plus = data['value']
                                        updated = True
                                    elif field == 'instagram':
                                        project.instagram = data['value']
                                        updated = True
                                    elif field == 'pinterest':
                                        project.pinterest = data['value']
                                        updated = True
                                    elif field == 'twitter':
                                        project.twitter = data['value']
                                        updated = True

                                if updated:
                                    project.save()

                                return {'success': True}
                        else:
                                return {'success': False, 'message': 'No data in request'}
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}
                except IntegrityError:
                    return {'success': False, 'message': 'User already assigned to project'}

@ajax
@csrf_protect
def follow_project(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST:
                try:
                    if 'follow' in request.POST and 'project' in request.POST:
                        follow = json.loads(request.POST['follow'])
                        project = Project.objects.get(id=request.POST['project'])
                        request_user = project.projectcreator_set.get(creator_id=request.user.id)

                        if follow is True:
                            Follower.objects.get_or_create(project=project, user=request_user, data=datetime.now())
                        else:
                            project_follow = Follower.objects.get(project=project, user=request_user)
                            project_follow.delete()

                    return {'success': True}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}
                except IntegrityError:
                    return {'success': False, 'message': 'User already assigned to project'}


@ajax
@csrf_protect
def add_post(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    request_user = project.projectcreator_set.get(creator_id=request.user.id)

                    if request_user.is_admin:
                        new_post = Post(author=request.user, project=project)
                        new_post.save()
                        return {'success': True, 'post_id': new_post.id, 'date_added': new_post.date_added.strftime("%d/%m/%Y"),
                                'month': new_post.date_added.strftime("%B")}
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}
                except IntegrityError:
                    return {'success': False, 'message': 'User already assigned to project'}

@ajax
@csrf_protect
def update_post(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    request_user = project.projectcreator_set.get(creator_id=request.user.id)

                    if request_user.is_admin:
                        updated = False

                        if 'data' in request.POST:
                            data = json.loads(request.POST['data'])

                            if 'field' in data and 'post' in data:
                                post = Post.objects.get(id=data['post'], project=project)
                                field = data['field']

                                if field == 'post' and 'body' in request.POST:
                                    post.post = request.POST['body']
                                    updated = True
                                elif field == 'title' and 'body' in request.POST:
                                    post.title = request.POST['body']
                                    updated = True
                                elif field == 'published' and 'value' in data:
                                    post.is_published = data['value']
                                    updated = True
                                elif field == 'author' and 'value' in data:
                                    author = User.objects.get(username=data['value'])
                                    post.author = author
                                    updated = True

                                if updated:
                                    post.save()

                                return {'success': True}
                        else:
                            return {'success': False, 'message': 'No data in request'}
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}
                except IntegrityError:
                    return {'success': False, 'message': 'User already assigned to project'}

    return {'success': False, 'message': 'Invalid request'}

# @ajax
# todo looks like this is not being sent as a ajax request
@csrf_protect
def image_upload(request):
    if request.method == "POST":
        # if request.is_ajax(): todo
            if 'project' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    request_user = project.projectcreator_set.get(creator_id=request.user.id)

                    if request_user.is_admin:
                        if len(request.FILES) == 1:
                            if 'logo' in request.POST and json.loads(request.POST['logo']) is True:
                                if project.logo is not None:
                                    project.logo.delete()

                                project.logo = request.FILES.get('file')
                                project.save()
                                data = {'success': True, 'link': project.logo.url}
                            else:
                                image = ProjectImage.objects.create(project=project, image=request.FILES.get('file'))
                                data = {'success': True, 'link': image.image.url}
                            return HttpResponse(json.dumps(data), content_type="application/json")
                            # return {'success': True, 'link': image.image.url}
                        else:
                            data = {'success': False, 'message':  'No image in request'}
                            return HttpResponse(json.dumps(data), content_type="application/json")

                    else:
                        data = {'success': False, 'message':  'Only admins can make an update to a project'}
                        return HttpResponse(json.dumps(data), content_type="application/json")

                except ObjectDoesNotExist:
                    data = {'success': False, 'message': 'Object does not exist'}
                    return HttpResponse(json.dumps(data), content_type="application/json")

                except IntegrityError as e:
                    data = {'success': False, 'message': 'Image already assigned to project'}
                    return HttpResponse(json.dumps(data), content_type="application/json")

    data = {'success': False, 'message': 'Invalid request'}
    return HttpResponse(json.dumps(data), content_type="application/json")


@ajax
@csrf_protect
def image_delete(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    request_user = project.projectcreator_set.get(creator_id=request.user.id)

                    if request_user.is_admin:
                        if 'src' in request.POST:
                            if 'logo' in request.POST and json.loads(request.POST['logo']) is True:
                                project.logo.delete()
                                project.save()
                            else:
                                image = ProjectImage.objects.get(project=project, image=request.POST['src'])
                                image.delete()

                            return {'success': True}
                        else:
                            return {'success': False, 'message':  'No url in request'}
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}
                except IntegrityError:
                    return {'success': False, 'message': 'Image already assigned to project'}

    return {'success': False, 'message': 'Invalid request'}


@ajax
@csrf_protect
def add_creator(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST and 'username' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    request_user = project.projectcreator_set.get(creator_id=request.user.id)

                    if request_user.is_admin:
                        user = User.objects.get(username=request.POST['username'])
                        ProjectCreator.objects.create(project=project, creator=user)
                        return {'success': True}
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}
                except IntegrityError:
                    return {'success': False, 'message': 'User already assigned to project'}

    return {'success': False, 'message': 'Invalid request'}


@ajax
@csrf_protect
def remove_creator(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST and 'username' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    request_user = project.projectcreator_set.get(creator_id=request.user.id)

                    if request_user.is_admin:
                        user = User.objects.get(username=request.POST['username'])
                        creator = ProjectCreator.objects.get(project=project, creator=user)
                        creator.delete()
                        return {'success': True}
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}
                except IntegrityError:
                    return {'success': False, 'message': 'User already assigned to project'}

    return {'success': False, 'message': 'Invalid request'}

@ajax
@csrf_protect
def update_creator(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST and 'username' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    request_user = project.projectcreator_set.get(creator_id=request.user.id)

                    if request_user.is_admin:
                        user = User.objects.get(username=request.POST['username'])
                        creator = ProjectCreator.objects.get(project=project, creator=user)
                        updated = False

                        if 'field' in request.POST:
                            if request.POST['field'] == 'summary' and 'body' in request.POST:
                                creator.summary = request.POST['body']
                                updated = True
                            elif request.POST['field'] == 'admin' and 'value' in request.POST:
                                creator.is_admin = request.POST['value']
                                updated = True

                        if updated:
                            creator.save()

                        return {'success': True}
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}
                except IntegrityError:
                    return {'success': False, 'message': 'User already assigned to project'}

    return {'success': False, 'message': 'Invalid request'}

# todo refactor the below ajax functions
@ajax
@csrf_protect
def add_technology(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST and 'technology' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    creator = project.projectcreator_set.get(creator_id=request.user.id)

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


@ajax
@csrf_protect
def remove_technology(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST and 'technology' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    creator = project.projectcreator_set.get(creator_id=request.user.id)

                    if creator.is_admin:
                        technology = Technologies.objects.get(name=request.POST['technology'])
                        project_technology = ProjectTechnologies.objects.get(project=project, technology=technology)
                        project_technology.delete()
                        return {'success': True}
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}

    return {'success': False, 'message': 'Invalid request'}


@ajax
@csrf_protect
def add_tag(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST and 'tag' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    creator = project.projectcreator_set.get(creator_id=request.user.id)

                    if creator.is_admin:
                        tag, created = Tags.objects.get_or_create(name=request.POST['tag'])
                        project.tags.add(tag)
                        return {'success': True}
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}
                except IntegrityError:
                    return {'success': False, 'message': 'Tag already assigned to project'}
                except Exception as e:
                    pass

    return {'success': False, 'message': 'Invalid request'}


@ajax
@csrf_protect
def remove_tag(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST and 'tag' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    creator = project.projectcreator_set.get(creator_id=request.user.id)

                    if creator.is_admin:
                        tag = Tags.objects.get(name=request.POST['tag'])
                        project.tags.remove(tag)
                        return {'success': True}
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}

    return {'success': False, 'message': 'Invalid request'}



