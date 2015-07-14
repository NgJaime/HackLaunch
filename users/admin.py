from django.contrib import admin
from users.models import Skill, MakerTypes, User, UserProfile
from user_activity_models import UserActivity

admin.site.register(UserActivity)
admin.site.register(Skill)
admin.site.register(MakerTypes)
admin.site.register(User)
admin.site.register(UserProfile)
