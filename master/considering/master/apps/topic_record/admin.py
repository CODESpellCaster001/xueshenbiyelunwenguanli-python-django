from django.contrib import admin
from .models import TopicRecord


# Register your models here.
class TopicRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_time')
    ordering = ('id',)


admin.site.register(TopicRecord, TopicRecordAdmin)
