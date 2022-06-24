# from pyexpat import model
# from re import T
# from statistics import mode
import re
from django.db import models
import event

from users.models import Profile

# Create your models here.

class Event(models.Model):
    status_choices=(
        ('approved','approved'),
        ('rejected','rejected'),
        ('waiting','waiting')
    )

    event_name=models.CharField(max_length=100)
    venue=models.CharField(max_length=200)
    event_description=models.CharField(max_length=500)
    contact_mobile=models.IntegerField(null=True,blank=True)
    contact_email=models.EmailField(null=True,blank=True)
    from_date=models.DateField()
    to_date=models.DateField()
    event_duration=models.IntegerField(null=True,blank=True)
    requested_by=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='requested_by')
    requested_on_behalf_of=models.CharField(max_length=100,null=True,blank=True)
    requested_at=models.DateTimeField(auto_now_add=True)
    # is_approved=models.BooleanField(default=False)
    # approved_by=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='approved_by',null=True,blank=True)
    # approved_at=models.DateTimeField(null=True,blank=True)
    # is_rejected=models.BooleanField(default=False)
    # rejected_by=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='rejected_by',null=True,blank=True)
    # rejected_at=models.DateTimeField(null=True,blank=True)
    status=models.CharField(max_length=30,choices=status_choices,default='waiting')
    status_updated_by=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='status_updated_by',null=True,blank=True)
    status_updated_at=models.DateTimeField(null=True,blank=True)
    is_photographers_assigned=models.BooleanField(default=False,blank=True,null=True)
    is_photos_uploaded=models.BooleanField(default=False)
    cover_pic=models.ImageField(upload_to='event_images/',null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    #status

    def __str__(self):
        return '{}-{}'.format(self.event_name,self.from_date)

    class Meta:
        unique_together=['event_name','from_date','to_date']

class EventPhase(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    phase_name=models.CharField(max_length=60)
    event_phase_date=models.DateField()
    phase_start_time=models.TimeField(default="00:00:01")
    phase_end_time=models.TimeField(default="23:59:59")
    created=models.DateTimeField(auto_now_add=True)
    photographers=models.ManyToManyField(Profile)
    photographers_assigned_by=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='photographer_assigned_by',null=True,blank=True)



    def __str__(self):
        return '{}-{}'.format(self.event.event_name,self.phase_name)

    class Meta:
        unique_together=['event','phase_name','event_phase_date']

# class EventPhotographerAssignment(models.Model):
#     event_phase=models.ForeignKey(EventPhase,on_delete=models.CASCADE,related_name='event_phase')
#     photographers=models.ManyToManyField(Profile,null=True,blank=True)
#     assigned_by=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='photographer_assigned_by',null=True,blank=True)
#     created=models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return '{}-{}'.format(self.event_phase.event.event_name,self.event_phase.phase_name)

class EventPhotos(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='cover_photo')
    photo=models.ImageField(upload_to='event_images/')
    uploaded_by=models.ForeignKey(Profile,on_delete=models.CASCADE)
    uploaded_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.event_name



class EventPhotosLink(models.Model):
    event=models.OneToOneField(Event,on_delete=models.CASCADE)
    photos_link=models.CharField(max_length=600)
    uploaded_by=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{}-{}'.format(self.event.event_name,self.event.from_date)
