from django.contrib import admin
from api.models import Task, User, Channel

# Register your models here.
admin.site.register(Task)
admin.site.register(User)
admin.site.register(Channel)
