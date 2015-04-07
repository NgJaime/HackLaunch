import os
import uuid

def upload_image(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    name = uuid.uuid1()

    return 'profiles/%s%s' % (str(name), filename_ext.lower())
