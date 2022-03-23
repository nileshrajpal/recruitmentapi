from django.contrib import admin
from .models import User, Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'posted_by')


admin.site.register(Application, ApplicationAdmin)
