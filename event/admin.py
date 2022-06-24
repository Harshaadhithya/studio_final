from multiprocessing import Event
from django.contrib import admin
from .models import Event, EventPhase, EventPhotos, EventPhotosLink

# Register your models here.
admin.site.register(Event)
admin.site.register(EventPhase)
# admin.site.register(EventPhotographerAssignment)

admin.site.register(EventPhotosLink)
admin.site.register(EventPhotos)