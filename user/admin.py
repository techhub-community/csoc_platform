from django.contrib import admin

from .models import Program, User, Team, Member

admin.site.register(Program)
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Member)
