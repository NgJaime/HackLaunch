from django.db import models

from datetime import datetime

from users.models import User
from projects.models import Project


class UserActivity(models.Model):
    INFORMATION_EVENT = u'1'
    CREATED_PROJECT_EVENT = u'2'
    JOINED_PROJECT_EVENT = u'3'
    ALERT_EVENT = u'4'
    UPDATE_EVENT = u'5'

    EVENT_TYPE_CHOICES = (
        (INFORMATION_EVENT, u'information event'),
        (CREATED_PROJECT_EVENT, u'created project event'),
        (JOINED_PROJECT_EVENT, u'joined project event'),
        (ALERT_EVENT, u'alert event'),
        (UPDATE_EVENT, u'update event'),
    )

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project, null=True)
    date_created = models.DateField()
    event_type = models.CharField(max_length=1, choices=EVENT_TYPE_CHOICES, default='1')

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'

    def save(self, *args, **kw):
        self.date_created = datetime.now()
        super(UserActivity, self).save(*args, **kw)

    def __unicode__(self):
        return self.user.get_full_name() + ' [' + self.date_created.strftime("%d/%m/%Y") + ']'

    def get_activity_date(self):
        return self.date_created.strftime("%d/%m/%Y")

    def get_title(self):
        if self.event_type == self.CREATED_PROJECT_EVENT:
            return 'Created a new project'
        elif self.event_type == self.JOINED_PROJECT_EVENT:
            return 'Joined a new project'

    def get_body(self):
        if self.event_type == self.CREATED_PROJECT_EVENT:
            project_title = self.project.title

            if project_title:
                return 'Created the project ' + self.project.get_title_text()
            else:
                return 'Created a new project'
        elif self.event_type == self.JOINED_PROJECT_EVENT:
            project_title = self.project.title

            if project_title:
                return 'Joined the project ' + self.project.get_title_text()
            else:
                return 'Joined a new project'
