import json
from django.shortcuts import render_to_response, get_object_or_404, redirect, Http404
from django.views.decorators.csrf import csrf_protect
from django.views.generic.detail import DetailView
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from django_ajax.decorators import ajax
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.http import HttpResponse

from datetime import datetime, timedelta
from urlparse import urlparse

from projects.models import Project, ProjectCreator, Technologies, ProjectTechnologies, Post, ProjectImage, Follower,\
    ProjectCreatorInitialisation, Views
from users.models import User, Skill
from users.user_activity_models import UserActivity
from ajax_decorators import project_ajax_request
from sanatise_html import clean_rich_html, clean_simple_html


class ProjectListView(ListView):
    template_name = 'project_list.html'
    paginate_by = 25
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all()[:10]

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectListView, self).get_context_data(*args, **kwargs)
        context['popular_projects'] = [view.project for view in Views.objects.filter(date=datetime.now() - timedelta(hours=24)).order_by('count')[:10]]

        if len(context['popular_projects']) < 5:
            context['popular_projects'] = list(set(context['popular_projects'] + list(context['object_list'])))

        return context


class UserProjectsListView(ListView):
    template_name = 'user_projects.html'
    paginate_by = 25
    context_object_name = 'project_creator'

    def get_queryset(self):
        return ProjectCreator.objects.filter(creator__username=self.kwargs['slug'])

    def get_context_data(self, *args, **kwargs):
        context = super(UserProjectsListView, self).get_context_data(*args, **kwargs)
        context['following'] = Follower.objects.filter(user__username=self.kwargs['slug'])

        if len(context['object_list']) > 0:
            context['full_name'] = context['object_list'][0].creator.get_full_name()
        elif len(context['following']) > 0:
            context['full_name'] = context['following'][0].user.get_full_name()
        else:
            context['full_name'] = User.objects.get(username=self.kwargs['slug']).get_full_name()

        return context


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

        creators = self.object.projectcreator_set.all()
        context['creators'] = creators
        context['technologies'] = self.object.projecttechnologies_set.all()
        context['posts'] = self.object.post_set.all().order_by('-date_added')
        context['prior_creators'] = any(creator.is_active is False for creator in creators)

        try:
            self.object.projectcreator_set.get(creator=self.request.user, is_active=True,
                                               is_admin=True, awaiting_confirmation=False)
        except Exception as e:
            context['project_admin'] = False
        else:
            context['project_admin'] = True

        # Add to the view count
        project_view, created = Views.objects.get_or_create(project=self.object, date=datetime.date(datetime.now()))
        project_view.count += 1
        project_view.save()

        self.object.cumulative_view_count += 1
        self.object.save()

        return context


class ProjectPostView(DetailView):
    template_name = 'project_post.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectPostView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(project=self.object, slug=self.kwargs['post'])

        if len(context['posts']) == 0:
            raise Http404

        try:
            self.object.projectcreator_set.get(creator=self.request.user, is_active=True,
                                               is_admin=True, awaiting_confirmation=False)
        except Exception as e:
            context['project_admin'] = False
        else:
            context['project_admin'] = True

        # Add to the view count
        project_view, created = Views.objects.get_or_create(project=self.object, date=datetime.date(datetime.now()))
        project_view.count += 1
        project_view.save()

        self.object.cumulative_view_count += 1
        self.object.save()

        return context


def get_project_context(project):
    date = datetime.now().strftime("%d/%m/%Y")
    month = datetime.now().strftime("%B")
    # todo cache
    technologies = json.dumps(list(Skill.objects.values_list('name', flat=True)), ensure_ascii=False).encode('utf8')
    prior_creators = any(creator.is_active is False for creator in project.projectcreator_set.all())
    context = {'date': date, 'month': month, 'technologies': technologies, 'projectId': project.id, 'prior_creator': prior_creators}

    return context


@csrf_protect
def project_create(request):
    if request.method == "GET":
        new_project = Project.objects.create()
        new_creators = ProjectCreator.objects.create(project=new_project, creator=request.user, is_admin=True, is_owner=True, awaiting_confirmation=False)

        user_activity = UserActivity.objects.create(user=request.user, project=new_project, event_type=UserActivity.CREATED_PROJECT_EVENT)

        context = get_project_context(new_project)

        return render_to_response('project_edit.html',
                                  {'project': new_project,
                                   'project_creators': [new_creators],
                                   'project_technologies': [],
                                   'project_tags': [],
                                   'context': context},
                                  RequestContext(request))
    else:
        raise Http404()

@csrf_protect
def project_edit(request, slug):
    if request.method == "GET":
        current_project = get_object_or_404(Project, slug=slug)

        try:
            creator = ProjectCreator.objects.get(creator=request.user, project=current_project)

            if creator.is_admin:
                context = get_project_context(current_project)

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
    else:
        raise Http404()

@ajax
@csrf_protect
@csrf_protect
def follow_project(request):
    if request.method == "POST":
        if 'follow' in request.POST and 'project' in request.POST:
            follow = json.loads(request.POST['follow'])
            project = Project.objects.get(id=request.POST['project'])

            if follow is True:
                follow, created = Follower.objects.get_or_create(project=project, user=request.user)
                project.cumulative_followers_count += 1
                project.save()
            else:
                project_follow = Follower.objects.get(project=project, user=request.user)
                project_follow.delete()
                project.cumulative_followers_count -= 1
                project.save()

            return {'success': True}

# todo quite a bit of scope for refacoting in the below ajax end-points
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
                pitch = clean_simple_html(request.POST['body'])
                project.pitch = pitch
                updated = True
            elif field == 'tagline' and 'body' in request.POST:
                tag_line = clean_simple_html(request.POST['body'])
                project.tag_line = tag_line
                updated = True
            elif field == 'title' and 'body' in request.POST:
                title = clean_simple_html(request.POST['body'])
                project.title = title
                updated = True
            elif 'value' in request.POST['data']:
                valid = False

                url = urlparse(data['value'].encode('utf8'))

                if not url.scheme:
                    url = urlparse('http://' + data['value'].encode('utf8'))

                if (field == 'google-plus' and url.netloc == 'plus.google.com' or url.netloc == 'www.plus.google.com') \
                    and url.path != '' and url.path != '/':
                    valid = True;
                elif (url.netloc == 'www.' + field + '.com' or url.netloc == field + '.com') \
                    and url.path != '' and url.path != '/':
                    valid = True

                if valid:
                    if field == 'facebook':
                        project.facebook = url.geturl()
                        updated = True
                    elif field == 'google-plus':
                        project.google_plus = url.geturl()
                        updated = True
                    elif field == 'instagram':
                        project.instagram = url.geturl()
                        updated = True
                    elif field == 'pinterest':
                        project.pinterest = url.geturl()
                        updated = True
                    elif field == 'twitter':
                        project.twitter = url.geturl()
                        updated = True
                else:
                    return {'success': False, 'message': 'Invalid social media link'}

            if updated:
                project.save()

            return {'success': True}
        else:
            return {'success': False, 'message': 'No field in request'}
    else:
            return {'success': False, 'message': 'No data in request'}

@project_ajax_request
def update_repo(request, project, *args, **kwargs):
    if 'data' in request.POST:
        data = json.loads(request.POST['data'])

        if 'field' in data and 'value' in data:
            updated = False
            valid = False

            url = urlparse(data['value'].encode('utf8'))

            if not url.scheme:
                url = urlparse('http://' + data['value'].encode('utf8'))

            field = data['field']

            if (url.netloc == 'www.' + field + '.com' or url.netloc == field + '.com') \
                and url.path != '' and url.path != '/':
                valid = True

            if valid:
                if field == 'github':
                    project.github_repo = url.geturl()
                    updated = True
            else:
                return {'success': False, 'message': 'Invalid ' + field + ' link'}

            if updated:
                project.save()

            return {'success': True}
        else:
            return {'success': False, 'message': 'No repo in request'}
    else:
            return {'success': False, 'message': 'No data in request'}

@project_ajax_request
def update_post(request, project, *args, **kwargs):
    if 'data' in request.POST:
        data = json.loads(request.POST['data'])

        if 'field' in data and 'post' in data:
            post = Post.objects.get(id=data['post'], project=project)
            field = data['field']
            updated = False

            if field == 'post' and 'body' in request.POST:
                clean_post = clean_rich_html(request.POST['body'])
                post.post = clean_post
                updated = True
            elif field == 'title' and 'body' in request.POST:
                clean_title = clean_simple_html(request.POST['body'])
                post.title = clean_title
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

        return {"message": "Required data missing from request", "success": False}
    else:
        return {'success': False, 'message': 'No data in request'}

# todo django ajax placing all json in content dictionary which is not expected by froala
@csrf_protect
def image_upload(request):
    response_data = {}
    if request.method == "POST":
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

                            response_data['link'] = project.logo.url
                        else:
                            image = ProjectImage.objects.create(project=project, image=request.FILES.get('file'))
                            response_data['link'] = image.image.url
                    else:
                        response_data['error'] = 'No image in request'
                else:
                    response_data['error'] = 'Only admins can make an update to a project'
            except ObjectDoesNotExist:
                response_data['error'] = 'Object does not exist'
        else:
            response_data['error'] = "Required data missing from request"
    else:
        response_data['error'] = 'method not supported'

    return HttpResponse(json.dumps(response_data), content_type="application/json")


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
        creator, created = ProjectCreator.objects.get_or_create(project=project, creator=user)

        if created:
            creator_initialisation = ProjectCreatorInitialisation.initialise(creator)

            verification_url = request.get_host() + reverse('validate_creator', kwargs={'code': creator_initialisation.code})

            context = {
                'verification_url': verification_url,
                'project_url': request.get_host() + reverse('project_view', kwargs={'slug': project.slug}),
                'project_title': project.get_title_text()
            }

            html_message = get_template('creator_verification_email.html').render(Context(context))
            email = EmailMessage('You have been assigned to a project on Hacklaunch', html_message,
                                 to=[user.email], from_email=settings.EMAIL_FROM)
            email.content_subtype = 'html'
            email.send()

        if created:
            return {'success': True}
        else:
            return {'success': False, 'message': 'User already assigned to project'}

    return {'success': False, 'message': 'No username in request'}


def validate_creator(request, code):
    creator_initialisation = get_object_or_404(ProjectCreatorInitialisation, code=code)

    user_activity = UserActivity.objects.create(user=creator_initialisation.creator.creator,
                                                project=creator_initialisation.creator.project,
                                                event_type=UserActivity.JOINED_PROJECT_EVENT)

    creator_initialisation.creator.awaiting_confirmation = False
    creator_initialisation.creator.save()

    slug = creator_initialisation.creator.project.slug

    creator_initialisation.delete()

    return redirect('project_view', slug=slug)


@project_ajax_request
def remove_creator(request, project, *args, **kwargs):
    if 'username' in request.POST:
        user = User.objects.get(username=request.POST['username'])
        creator = ProjectCreator.objects.get(project=project, creator=user)
        creator.is_active = False
        creator.save()
        return {'success': True}

    return {'success': False, 'message': 'No username in request'}


@project_ajax_request
def update_creator(request, project, *args, **kwargs):
    if 'username' in request.POST:
        user = User.objects.get(username=request.POST['username'])
        creator = ProjectCreator.objects.get(project=project, creator=user)
        updated = False

        if 'field' in request.POST:
            if request.POST['field'] == 'summary' and 'body' in request.POST:
                summary = clean_simple_html(request.POST['body'])
                creator.summary = summary
                updated = True
            elif request.POST['field'] == 'admin' and 'value' in request.POST:
                creator.is_admin = json.loads(request.POST['value'])
                updated = True
            elif request.POST['field'] == 'active' and 'value' in request.POST:
                creator.is_active = json.loads(request.POST['value'])
                updated = True

            if updated:
                creator.save()
                return {'success': True}

    return {"message": "Required data missing from request", "success": False}


@project_ajax_request
def add_technology(request, project, *args, **kwargs):
    if 'technology' in request.POST:
        technology, created = Technologies.objects.get_or_create(name=request.POST['technology'])
        ProjectTechnologies.objects.create(project=project, technology=technology)
        return {'success': True}

    return {"message": "Required data missing from request", "success": False}


@project_ajax_request
def remove_technology(request, project, *args, **kwargs):
    if 'technology' in request.POST:
        technology = Technologies.objects.get(name=request.POST['technology'])
        project_technology = ProjectTechnologies.objects.get(project=project, technology=technology)
        project_technology.delete()
        return {'success': True}

    return {"message": "Required data missing from request", "success": False}


@project_ajax_request
def update_technology(request, project, *args, **kwargs):
    if 'technology' in request.POST and 'strength' in request.POST:
        technology = Technologies.objects.get(name=request.POST['technology'])
        project_technology = ProjectTechnologies.objects.get(project=project, technology=technology)
        project_technology.strength = request.POST['strength']
        project_technology.save()
        return {'success': True}

    return {"message": "Required data missing from request", "success": False}


@project_ajax_request
def add_tag(request, project, *args, **kwargs):
    if 'tag' in request.POST:
        project.tags.add(request.POST['tag'])
        return {'success': True}

    return {"message": "Required data missing from request", "success": False}


@project_ajax_request
def remove_tag(request, project, *args, **kwargs):
    if 'tag' in request.POST:
        project.tags.remove(request.POST['tag'])
        return {'success': True}

    return {"message": "Required data missing from request", "success": False}
