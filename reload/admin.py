#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin, sites
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.auth.models import User


################
##### LOGS #####

from django.contrib.admin.models import LogEntry

action_names = {
    ADDITION: 'Addition',
    CHANGE:   'Change',
    DELETION: 'Deletion',
}

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    list_filter = ['user','content_type',]
    search_fields = ['object_repr','change_message']
    list_display = ['action_time','user','content_type','object_link','action_description','change_message',]

    def object_link(self, obj):
        ct = obj.content_type
        repr_ = escape(obj.object_repr)
        try:
            href = reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id])
            link = u'<a href="%s">%s</a>' % (href, repr_)
        except NoReverseMatch:
            link = repr_
        return link if obj.action_flag != DELETION else repr_
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def action_description(self, obj):
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'

# admin.site.register(LogEntry, admin.ModelAdmin)
# admin.site.register(LogEntry, LogEntryAdmin)

# moje modyfikacje wyświetlania

from django.contrib.auth.admin import UserAdmin

# class MyUserAdmin(UserAdmin):
#     # override the default sort column
#     ordering = ('-date_joined', )
#     # if you want the date they joined or other columns displayed in the list,
#     # override list_display too
#     list_display = ('username', 'email', 'date_joined', 'last_login','first_name', 'last_name', 'is_staff')
#
# # finally replace the default UserAdmin with yours
# admin.site.unregister(User)
# admin.site.register(User, MyUserAdmin)

UserAdmin.ordering = ('-date_joined', )
UserAdmin.list_display = ('username', 'email', 'date_joined', 'last_login', 'is_staff')

from auditlog.admin import LogEntryAdmin
LogEntryAdmin.list_display = ['created', 'content_type', 'resource_url', 'action', 'msg_short', 'user_url']



#
# class LogEntryAdmin(admin.ModelAdmin, LogEntryAdminMixin):
#     list_display = ['created', 'resource_url', 'action', 'msg_short', 'user_url']
#     search_fields = ['timestamp', 'object_repr', 'changes', 'actor__first_name', 'actor__last_name']
#     list_filter = ['action', ResourceTypeFilter]
#     readonly_fields = ['created', 'resource_url', 'action', 'user_url', 'msg']
#     fieldsets = [
#         (None, {'fields': ['created', 'user_url', 'resource_url']}),
#         ('Changes', {'fields': ['action', 'msg']}),
#     ]





##################
##### RELOAD #####

from .models import caliber, powder, bullet, quality, score, loads, comment, test


@admin.register(caliber)
class caliberAdmin(admin.ModelAdmin):
    list_display = (u'id', u'caliber', u'comment', u'user', u'date',u'datemod')
    list_filter = ('user', u'date',u'datemod')


@admin.register(powder)
class powderAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        u'vendor',
        u'powder',
        u'comment',
        u'user',
        u'date',
        u'datemod',
    )
    list_filter = ('user', u'date')


@admin.register(bullet)
class bulletAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        u'caliber',
        u'vendor',
        u'bullet',
        u'weight',
        u'calibration',
        u'length',
        u'bc',
        u'comment',
        u'user',
        u'date',
        u'datemod',
    )
    list_filter = ('caliber', 'user', u'date')


@admin.register(quality)
class qualityAdmin(admin.ModelAdmin):
    list_display = (u'id', u'quality')


@admin.register(score)
class scoreAdmin(admin.ModelAdmin):
    list_display = (u'id', u'score')


@admin.register(loads)
class loadsAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        u'caliber',
        u'gun',
        u'bullet',
        u'powder',
        u'COL',
        u'load',
        u'crimp',
        u'prime',
        u'case',
        u'quality',
        u'votes',
        u'user',
        u'date',
        u'datemod',
    )
    list_filter = (u'date', u'datemod', 'user', )


@admin.register(comment)
class commentAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        u'load',
        u'date',
        u'datemod',
        u'gun',
        u'comment',
        u'score',
        u'user',
    )
    list_filter = ('load', u'date', 'score', 'user')


@admin.register(test)
class testAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        u'load',
        u'date',
        u'datemod',
        u'gun',
        u'v0t',
        u'v0c',
        u'temp',
        u'moa',
        u'comment',
        u'photo',
        u'user',
    )
    list_filter = ('load', u'date', 'user')
