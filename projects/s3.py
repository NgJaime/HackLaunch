import os
import uuid

# combine with profiel s3 file?
def upload_project_image(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    name = uuid.uuid1()

    return 'project/%s%s' % (str(name), filename_ext.lower())

def upload_logo(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    name = uuid.uuid1()

    return 'logos/%s%s' % (str(name), filename_ext.lower())

