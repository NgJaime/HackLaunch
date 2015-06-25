import os
import uuid

def upload_profile_image(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    name = uuid.uuid1()

    return 'profiles/%s%s' % (str(name), filename_ext.lower())


def upload_profile_thumbnail(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    name = uuid.uuid1()

    return 'profiles-thumbnail/%s%s' % (str(name), filename_ext.lower())


