from django.contrib import admin

from .models import Poll,Comment

# Register your models here.

admin.site.register(Poll)
admin.site.register(Comment)
