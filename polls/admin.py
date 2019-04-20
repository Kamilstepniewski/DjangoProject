from django.contrib import admin

from .models import Poll,Comment,Vote

# Register your models here.

admin.site.register(Poll)
admin.site.register(Comment)
admin.site.register(Vote)
