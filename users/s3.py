import os
from PIL import Image
from django.core.files.storage import default_storage as storage
from django.utils.timezone import now

def upload_image(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)

    return 'profiles/%s%s' % (now().strftime("%Y%m%d%H%M%S"), filename_ext.lower())

