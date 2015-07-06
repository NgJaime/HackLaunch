from functools import wraps
from django_ajax.decorators import ajax
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist


from projects.models import Project

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
