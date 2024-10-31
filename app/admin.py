from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Users)
class Users(admin.ModelAdmin):
    list_display = ("username", "email",)
    exclude = ("password",)


admin.site.register(models.Expnese)
admin.site.register(models.Income)
