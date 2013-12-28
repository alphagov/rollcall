from django.contrib import admin
from rollcall.groups.models import Group


class GroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(Group, GroupAdmin)
