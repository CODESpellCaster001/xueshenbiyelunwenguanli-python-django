from django.contrib import admin
from .models import Feedback2Teacher, Feedback2Student


# Register your models here.
class Feedback2TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'feedback')
    ordering = ('id',)


class Feedback2StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'feedback')
    ordering = ('id',)


admin.site.register(Feedback2Student, Feedback2StudentAdmin)
admin.site.register(Feedback2Teacher, Feedback2TeacherAdmin)
