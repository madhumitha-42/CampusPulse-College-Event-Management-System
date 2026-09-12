from django.contrib import admin

from .models import Category, Event, Registration, User

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Registration)