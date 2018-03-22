from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Team, TeamMember, Task


admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Task)
admin.site.register(Permission)
