from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(AdminLaser)
admin.site.register(Client)
admin.site.register(Fields)
admin.site.register(LaserRep)
admin.site.register(JobStatus)
admin.site.register(Dataset)
admin.site.register(FeedBackClient)
admin.site.register(NotificationClient)
admin.site.register(Payment)
