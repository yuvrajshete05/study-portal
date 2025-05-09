from django.contrib import admin
from . models import * 

# Register your models here.

admin.site.register(Notes)       # for show the table in admin page
admin.site.register(Homework)    # for show the table in admin page
admin.site.register(Todo)        # for show the table in admin page
