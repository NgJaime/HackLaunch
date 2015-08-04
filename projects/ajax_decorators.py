import json
from functools import wraps
from django_ajax.decorators import ajax
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from projects.models import Project
from urlparse import urlparse


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
            else:
                {"message": "Required data missing from request", "success": False}
    return wrapped


def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        elif 'HTTP_REFERER' in request.META:
            referer = urlparse(request.META['HTTP_REFERER'])
            json_data = json.dumps({'status': 401, 'message': 'Login required', 'redirect': 'login/?next=' + referer.path})
            return HttpResponse(json_data, content_type='application/json')
        else:
            json_data = json.dumps({'status': 401, 'message': 'Login required'})
            return HttpResponse(json_data, content_type='application/json')
    return wrapper
