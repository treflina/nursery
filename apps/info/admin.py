from django.contrib import admin

from .models import Activities, MainTopic, Menu, Note

admin.site.register(Menu)
admin.site.register(Note)
admin.site.register(Activities)
admin.site.register(MainTopic)
