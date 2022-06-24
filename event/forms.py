from dataclasses import fields
from pyexpat import model
from statistics import mode
from django import forms
from django.forms import ModelForm
from .models import *
from django import forms
import datetime

class EventRequestForm(ModelForm):
    class Meta:
        model=Event
        fields=['event_name','venue','event_description','from_date','to_date','requested_on_behalf_of','contact_mobile','contact_email']
        labels={'requested_on_behalf_of':'Club/Organisation Name'}
        widgets = {
        'from_date': forms.DateInput(attrs={ 'type':'date','min':datetime.date.today()}),
        'to_date': forms.DateInput(attrs={ 'type':'date','min':datetime.date.today()}), 
        'event_description':forms.Textarea(attrs={'rows':4})  
    }

    def __init__(self,*args,**kwargs):
        super(EventRequestForm,self).__init__(*args,**kwargs)
        self.fields['event_name'].widget.attrs.update({'class':'input-responsive'})
        self.fields['venue'].widget.attrs.update({'class':'input-responsive'})
        self.fields['event_description'].widget.attrs.update({'class':'input-responsive'})
        self.fields['requested_on_behalf_of'].widget.attrs.update({'class':'input-responsive'})
        self.fields['from_date'].widget.attrs.update({'class':'input-responsive'})
        self.fields['to_date'].widget.attrs.update({'class':'input-responsive'})
        self.fields['contact_mobile'].widget.attrs.update({'class':'input-responsive'})
        self.fields['contact_email'].widget.attrs.update({'class':'input-responsive'})
        

class EventPhaseForm(ModelForm):
    class Meta:
        model=EventPhase
        fields='__all__'
        exclude=['event','photographers','photographers_assigned_by']

class AssignPhotographerForm(ModelForm):
    class Meta:
        model=EventPhase
        fields='__all__'
        exclude=['event','photographers_assigned_by']
        widgets={
            'photographers':forms.CheckboxSelectMultiple()
            }
            
class EventPhotoForm(ModelForm):
    class Meta:
        model=EventPhotos
        fields=['photo','uploaded_by']

class EvevntPhotosLinkForm(ModelForm):
    class Meta:
        model=EventPhotosLink
        fields=['photos_link']