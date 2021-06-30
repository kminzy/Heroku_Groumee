from django.contrib import admin
from .models import User, Schedule, Group, GroupSchedule

# Register your models here.
admin.site.register(User)
admin.site.register(Schedule)
admin.site.register(Group)
admin.site.register(GroupSchedule)