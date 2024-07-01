from django.contrib import admin
from .models import Annex


# Register your models here.
class AnnexAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'raw_name', 'uploader')
    ordering = ('id',)


admin.site.register(Annex, AnnexAdmin)
