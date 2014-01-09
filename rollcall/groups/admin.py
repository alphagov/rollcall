from django.contrib import admin
from rollcall.groups.models import Group, Membership


class GroupAdmin(admin.ModelAdmin):
    pass


class MembershipAdmin(admin.ModelAdmin):
    pass


admin.site.register(Group, GroupAdmin)
admin.site.register(Membership, MembershipAdmin)
