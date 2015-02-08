from django.contrib import admin
from exam.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import gettext as _
# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    max_num = 10
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    max_num = 90

class TestAdmin(ImportExportModelAdmin):
    list_display = ('name', 'branch_code', 's_id')
    inlines = [QuestionInline]

class QuestionAdmin(ImportExportModelAdmin):
    list_display = ('title', 'correct_answer', 'test', 'ss_id')
    inlines = [AnswerInline]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'ques', 'ans')


class Score_CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Score_Card, Score_CardAdmin)
admin.site.register(Choice, ChoiceAdmin)