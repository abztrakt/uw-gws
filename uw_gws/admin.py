from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import GroupManager
from django.db import models

# Utils.py contains the get request needed to process the information.
import utils


# Modify the actions available for groups in the admin interface.
class GroupAdmin(admin.ModelAdmin):
    actions = ['update_group']
    filter_horizontal = ('permissions',)

    def update_group(self,request,queryset):
        count = 0
        for group in queryset:
            update = utils.update_group_members(group.name)
            if update['is_updated']:
                count += 1

        if count == 0:
            message_bit = "No groups were"
        elif count == 1:
            message_bit = "1 group was"
        else:
            message_bit = "%d groups were" % (count)

        self.message_user(request, "%s successfully updated." % message_bit)
    update_group.short_description = "Update selected groups"

admin.site.unregister(Group)
admin.site.register(Group,GroupAdmin)
