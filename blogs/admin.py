from django.contrib import admin
from blogs import models
# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Post)
admin.site.register(models.Comment)
