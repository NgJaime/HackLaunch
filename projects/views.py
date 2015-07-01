import json
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.template import RequestContext
from django_ajax.decorators import ajax
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from django.views.generic import ListView

from functools import wraps
from datetime import datetime
from projects.models import Project, ProjectCreator, Technologies, ProjectTechnologies, Post, ProjectImage, Follower
from users.models import User, Skill



class PostListView(ListView):
    template_name = 'project_list.html'
    paginate_by = 25
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all()


class ProjectView(DetailView):
    template_name = 'project_view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)

        if self.request.user.is_anonymous():
            context['follower'] = False
        else:
            follower = Follower.objects.filter(project=self.object, user=self.request.user)
            context['follower'] = True if len(follower) == 1 else False

        context['creators'] = self.object.projectcreator_set.all()
        context['technologies'] = self.object.projecttechnologies_set.all()
        context['posts'] = self.object.post_set.all()

        return context


def get_project_context(project_id):
    date = datetime.now().strftime("%d/%m/%Y")
    month = datetime.now().strftime("%B")
    # todo cache
    technologies = json.dumps(list(Skill.objects.values_list('name', flat=True)), ensure_ascii=False).encode('utf8')
    context = {'date': date, 'month': month, 'technologies': technologies, 'projectId': project_id}

    return context


@csrf_protect
def project_create(request):
    if request.method == "GET":
        new_project = Project.objects.create()
        new_creators = ProjectCreator.objects.create(project=new_project, creator=request.user, is_admin=True, is_owner=True, awaiting_confirmation=False)
        context = get_project_context(new_project.id)

        return render_to_response('project_edit.html',
                                  {'project': new_project,
                                   'project_creators': [new_creators],
                                   'project_technologies': [],
                                   'project_tags': [],
                                   'context': context},
                                  RequestContext(request))


@csrf_protect
def project_edit(request, slug):
    if request.method == "GET":
        current_project = get_object_or_404(Project, slug=slug)

        try:
            creator = ProjectCreator.objects.get(creator=request.user, project=current_project)

            if creator.is_admin:
                context = get_project_context(current_project.id)

                creators = ProjectCreator.objects.filter(project=current_project.id).order_by('date_joined')
                posts = Post.objects.filter(project=current_project).order_by('-date_added')

                return render_to_response('project_edit.html',
                                          {'project': current_project,
                                           'project_creators': creators,
                                           'project_posts': posts,
                                           'project_technologies': current_project.projecttechnologies_set.all(),
                                           'project_tags': ','.join(current_project.tags.values_list('name', flat=True)),
                                           'context': context},
                                          RequestContext(request))
            else:
                return redirect('/projects/' + slug)
        except ObjectDoesNotExist:
                return redirect('/projects/' + slug)

@ajax
@csrf_protect
def follow_project(request):
    if request.method == "POST":
        if request.is_ajax():
            if 'project' in request.POST:
                if 'follow' in request.POST and 'project' in request.POST:
                    follow = json.loads(request.POST['follow'])
                    project = Project.objects.get(id=request.POST['project'])

                    if follow is True:
                        follow, created = Follower.objects.get_or_create(project=project, user=request.user)
                    else:
                        project_follow = Follower.objects.get(project=project, user=request.user)
                        project_follow.delete()

                return {'success': True}


def project_ajax_request(function):
    @ajax(mandatory=False)
    @csrf_protect
    @wraps(function)
    def wrapped(request, *args, **kwargs):
        if request.method == "POST":
            if 'project' in request.POST:
                try:
                    project = Project.objects.get(id=request.POST['project'])
                    request_user = project.projectcreator_set.get(creator_id=request.user.id)

                    if request_user.is_admin:
                        return function(request, project, args, kwargs)
                    else:
                        return {'success': False, 'message':  'Only admins can make an update to a project'}

                except ObjectDoesNotExist:
                    return {'success': False, 'message': 'Object does not exist'}
                except IntegrityError:
                    return {'success': False, 'message': 'User already assigned to project'}

    return wrapped


@project_ajax_request
def add_post(request, project, *args, **kwargs):
    new_post = Post(author=request.user, project=project)
    new_post.save()
    return {'success': True, 'post_id': new_post.id, 'date_added': new_post.date_added.strftime("%d/%m/%Y"),
            'month': new_post.date_added.strftime("%B")}


@project_ajax_request
def update_project(request, project, *args, **kwargs):
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


@project_ajax_request
def update_post(request, project, *args, **kwargs):
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


@project_ajax_request
def image_upload(request, project, *args, **kwargs):
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


@project_ajax_request
def image_delete(request, project, *args, **kwargs):
    if 'src' in request.POST:
        if request.POST['src'] != [u'/static/images/add-a-logo.png'] and\
                'logo' in request.POST and json.loads(request.POST['logo']) is True:
            project.logo.delete()
            project.save()
        else:
            image = ProjectImage.objects.get(project=project, image=request.POST['src'])
            image.delete()

        return {'success': True}
    else:
        return {'success': False, 'message': 'No url in request'}


@project_ajax_request
def add_creator(request, project, *args, **kwargs):
    if 'username' in request.POST:
        user = User.objects.get(username=request.POST['username'])
        ProjectCreator.objects.create(project=project, creator=user)
        return {'success': True}


@project_ajax_request
def remove_creator(request, project, *args, **kwargs):
    if 'username' in request.POST:
        user = User.objects.get(username=request.POST['username'])
        creator = ProjectCreator.objects.get(project=project, creator=user)
        creator.delete()
        return {'success': True}


@project_ajax_request
def update_creator(request, project, *args, **kwargs):
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


@project_ajax_request
def add_technology(request, project, *args, **kwargs):
    if 'technology' in request.POST:
        technology, created = Technologies.objects.get_or_create(name=request.POST['technology'])
        ProjectTechnologies.objects.create(project=project, technology=technology)
        return {'success': True}


@project_ajax_request
def remove_technology(request, project, *args, **kwargs):
    if 'technology' in request.POST:
        technology = Technologies.objects.get(name=request.POST['technology'])
        project_technology = ProjectTechnologies.objects.get(project=project, technology=technology)
        project_technology.delete()
        return {'success': True}


@project_ajax_request
def add_tag(request, project, *args, **kwargs):
    if 'tag' in request.POST:
        project.tags.add(request.POST['tag'])
        return {'success': True}


@project_ajax_request
def remove_tag(request, project, *args, **kwargs):
    if 'tag' in request.POST:
        project.tags.remove(request.POST['tag'])
        return {'success': True}
