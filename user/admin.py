__author__ = 'sgupta'
from django.contrib import admin
from user.models import *


class ProjectsInline(admin.TabularInline):
    model = ProjectDetails
    extra = 0
    max_num = 5


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'dob', 'cv', 'avatar_url' )
    inlines = [ProjectsInline]



admin.site.register(UserProfile, UserProfileAdmin)