
from django.contrib import admin

from task.models import Task
from user.models import User

admin.site.register(User)
admin.site.register(Task)