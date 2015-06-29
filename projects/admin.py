from django.contrib import admin
from projects.models import Project, ProjectCreator, ProjectTechnologies, Technologies, Post, ProjectImage, Follower

admin.site.register(ProjectCreator)
admin.site.register(ProjectTechnologies)
admin.site.register(Technologies)
admin.site.register(Post)
admin.site.register(ProjectImage)
admin.site.register(Follower)


class CreatorsInline(admin.TabularInline):
    model = ProjectCreator

class ProjectAdmin(admin.ModelAdmin):
    inlines = [CreatorsInline,]
    exclude = ('elements',) #exclude the field you put the inline on so you dont have double fields

admin.site.register(Project, ProjectAdmin)
