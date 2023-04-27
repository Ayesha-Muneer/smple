from django.contrib import admin

# Register your models here.
from LeakDetectionApp import models

admin.site.register(models.Login)
admin.site.register(models.Consumer)
admin.site.register(models.Worker)
admin.site.register(models.Schedule)
