from django.contrib import admin
from users.models import Skill, MakerTypes, User, UserProfile

admin.site.register(Skill)
admin.site.register(MakerTypes)
admin.site.register(User)
admin.site.register(UserProfile)
