from django.contrib import admin
from .models import AnnexPhase, UserPhase


# Register your models here.
class AnnexPhaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'annex_phase')


class UserPhaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_phase')


admin.site.register(AnnexPhase, AnnexPhaseAdmin)
admin.site.register(UserPhase, UserPhaseAdmin)
