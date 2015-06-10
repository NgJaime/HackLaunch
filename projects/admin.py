from django.contrib import admin
from projects.models import Project, ProjectCreators, ProjectTechnologies, Technologies, Tags

# admin.site.register(Project)
admin.site.register(ProjectCreators)
admin.site.register(ProjectTechnologies)
admin.site.register(Technologies)
admin.site.register(Tags)


class CreatorsInline(admin.TabularInline):
    model = Project.creators.through

class ProjectAdmin(admin.ModelAdmin):
    inlines = [CreatorsInline,]
    exclude = ('elements',) #exclude the field you put the inline on so you dont have double fields

admin.site.register(Project, ProjectAdmin)
