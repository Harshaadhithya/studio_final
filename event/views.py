
from email import message
from multiprocessing import context
from django.contrib import messages

from django.shortcuts import redirect, render

from datetime import datetime

from django.contrib.auth.decorators import login_required

from .forms import *

# Create your views here.
@login_required(login_url='user-login')
def hire_us(request):
    form=EventRequestForm()
    context={'form':form}
    if request.method=='POST':
        form=EventRequestForm(request.POST)
        if form.is_valid():
            EventRequestObj=form.save(commit=False)
            start_date=request.POST['from_date']
            end_date=request.POST['to_date']
            start_date=datetime.datetime.strptime(start_date,"%Y-%m-%d")
            end_date=datetime.datetime.strptime(end_date,"%Y-%m-%d")
            day_difference=(end_date-start_date)
            event_duration=(day_difference.days)+1
            EventRequestObj.event_duration=event_duration
            EventRequestObj.requested_by=request.user.profile
            EventRequestObj.requested_at=datetime.datetime.today()
            # for i in range(0,event_duration):
            #         print(start_date+datetime.timedelta(days=int(i)))
            #         print(i)
            try:
                EventRequestObj.save()
                phase_objs_list=[]
                phase_forms_list=[]
                for i in range(0,event_duration):
                    event_phase_date=start_date+datetime.timedelta(days=int(i)) 
                    event_phase_obj=EventPhase.objects.create(event=EventRequestObj,phase_name='day-{}'.format(i+1),event_phase_date=event_phase_date)
                    # phase_objs_list.append(event_phase_obj)
                return redirect('event_phase_allocation',pk=EventRequestObj.id)

                # for i,phase_obj in enumerate(phase_objs_list):
                #     phase_form=EventPhaseForm(instance=phase_obj,prefix="phase_form-{}".format(i))
                #     phase_forms_list.append(phase_form)
                # context={'phase_forms_list':phase_forms_list}

                
                # phase_form=EventPhaseForm(insta)
            except:
                pass
        return redirect('home')

    
    return render(request,'event/hireus1.html',context)

def event_phase_allocation(request,pk):
    context={}
    EventRequestObj=Event.objects.get(id=pk)
    phase_forms_list=[]
    event_phase_objs_list=EventRequestObj.eventphase_set.all()
    for i,event_phase_obj in enumerate(event_phase_objs_list):
        phase_form=EventPhaseForm(request.POST or None,instance=event_phase_obj,prefix="phase_form_{}".format(i))
        phase_forms_list.append(phase_form)
    context={'phase_forms_list':phase_forms_list}

    if request.method=='POST':
        form_flag=1
        for each_form in phase_forms_list:
            if each_form.is_valid():
                print("valid form")
            else:
                form_flag=0
                print("not valid")
                break

        if form_flag==1:
            for each_form in phase_forms_list:
                print("each_form",each_form)
                each_form.save()
        else:
            print("error in phase form")
        return redirect('home')
    return render(request,'event/phase_allocation_form.html',context)

@login_required(login_url='user-login')
def admin_events_list(request,event_list_type='upcoming'):
    if request.user.profile.role=='admin':
        page=event_list_type
        context={'page':event_list_type}
        today=datetime.datetime.today()
        if event_list_type=='all':
            event_objs=Event.objects.exclude(status='waiting').order_by('-from_date')
            print(event_objs)
        elif event_list_type=='upcoming':
            event_objs=Event.objects.filter(from_date__gte = today).order_by('from_date')
            print(event_objs)
        elif event_list_type=='completed':
            event_objs=Event.objects.filter(to_date__lt = today,status='approved').order_by('-to_date')
            print(event_objs)
        elif event_list_type=='approved':
            event_objs=Event.objects.filter(from_date__gte = today,status='approved').order_by('from_date')
            print(event_objs)
        elif event_list_type=='yet_to_be_approved':
            event_objs=Event.objects.filter(from_date__gte = today,status='waiting').order_by('from_date')
            print(event_objs)
        elif event_list_type=='rejected':
            event_objs=Event.objects.filter(status='rejected').order_by('-from_date')
            print(event_objs)
        else:
            messages.error(request,"invalid event type")
            return redirect('home') 
        context['event_objs']=event_objs   
        return render(request,'event/admin_events_list.html',context)
    else:
        messages.error(request,"You are not authorised!")
        return redirect('home')

def view_events_list_by_user(request):
    context={}
    events_list=Event.objects.filter(status='approved',is_photos_uploaded=True)
    context['events_list']=events_list
    return render(request,'event/event_list_for_user.html',context)

@login_required(login_url='user-login')
def approve_event(request,pk):
    if request.user.profile.role=='admin':
        event_obj=Event.objects.get(id=pk)
        event_obj.status='approved'
        event_obj.status_updated_by=request.user.profile
        event_obj.status_updated_at=datetime.datetime.now()
        event_obj.save()
        return redirect('admin_events_list',event_list_type='yet_to_be_approved')
    else:
        messages.error(request,"You are not authorised!")
        return redirect('home')

@login_required(login_url='user-login')
def reject_event(request,pk):
    if request.user.profile.role=='admin':
        event_obj=Event.objects.get(id=pk)
        # event_obj.status='rejected'
        event_obj.status='rejected'
        event_obj.status_updated_by=request.user.profile
        event_obj.status_updated_at=datetime.datetime.now()
        event_obj.is_photographers_assigned=False
        
        event_obj.save()
        event_phase_objs=event_obj.eventphase_set.all()
        for event_phase_obj in event_phase_objs:
            # event_phase_obj.photographers=None
            event_phase_obj.photographers.clear()
            event_phase_obj.photographers_assigned_by=None
            event_phase_obj.save()
        return redirect('admin_events_list',event_list_type='yet_to_be_approved')
    else:
        messages.error(request,"You are not authorised")
        return redirect('home')

@login_required(login_url='user-login')
def assign_photographers(request,pk):
    if request.user.profile.role=='admin':
        phase_forms_list=[]
        event_obj=Event.objects.get(id=pk)
        event_phase_objs=event_obj.eventphase_set.all()
        for i,event_phase_obj in enumerate(event_phase_objs):
            phase_form=AssignPhotographerForm(request.POST or None,instance=event_phase_obj,prefix="assign_photographer_form_{}".format(i))
            phase_forms_list.append(phase_form)
        context={'phase_forms_list':phase_forms_list}

        if request.method=='POST':
            form_flag=1
            for each_form in phase_forms_list:
                if each_form.is_valid():
                    print("valid form")
                else:
                    form_flag=0
                    print("not valid")
                    break

            if form_flag==1:
                for each_form in phase_forms_list:
                    # print("each_form",each_form)
                    event_phase_obj=each_form.save(commit=False)
                    event_phase_obj.photographers_assigned_by=request.user.profile
                    event_phase_obj.save()
                    each_form.save_m2m()
                event_obj.is_photographers_assigned=True
                event_obj.save()
            else:
                print("error in phase form")
            return redirect('home')
        return render(request,'event/assign_photographers_form.html',context)
    else:
        messages.error(request,"You are not authorised!")
        return redirect('home')

@login_required(login_url='user-login')
def upload_event_photos(request,pk):
    if request.user.profile.role=='admin' or request.user.profile.role=='photographer':
        context={}
        event_obj=Event.objects.get(id=pk)
        context['event_obj']=event_obj
        event_photo_objs_length=len(EventPhotos.objects.filter(event=event_obj))
        print(event_photo_objs_length)
        if request.method=='POST':
            images=request.FILES.getlist('uploaded_images')
            print(len(images))
            if (event_photo_objs_length+len(images))<=6:
                for image in images:
                    event_photo_obj=EventPhotos.objects.create(event=event_obj,photo=image,uploaded_by=request.user.profile)
                messages.success(request,'photos uploaded successfully')
                event_photos_link=request.POST['event_photos_link']
                if event_photos_link!='':
                    event_photos_link_obj=EventPhotosLink.objects.create(event=event_obj,photos_link=event_photos_link,uploaded_by=request.user.profile)
                    event_obj.is_photos_uploaded=True
                    cover_photo_obj=EventPhotos.objects.filter(event=event_obj).first()
                    event_obj.cover_pic=cover_photo_obj.photo
                    print(event_obj.cover_pic)
                    event_obj.save()
                
            else:
                if EventPhotos.objects.filter(event=event_obj).exists():
                    event_obj.is_photos_uploaded=True
                    cover_photo_obj=EventPhotos.objects.filter(event=event_obj).first()
                    event_obj.cover_pic=cover_photo_obj.photo
                    print(event_obj.cover_pic)

                    event_obj.save()
                messages.error(request,"You have already uploaded {} photos to {} event, now you are trying to upload {} photos which exceeds the total limit of 6 photos per event!".format(event_photo_objs_length,event_obj.event_name,len(images)))
                return redirect(upload_event_photos,pk=event_obj.id)

        return render(request,'event/upload_photos_form.html',context)
    else:
        messages.error(request,"You are not authorised!")
        return redirect('home')

# @login_required(login_url='user-login')
def view_event_photos(request,pk):
    event_obj=Event.objects.get(id=pk)
    event_photo_objs=EventPhotos.objects.filter(event=event_obj)
    context={'event_photo_objs':event_photo_objs,'event_obj':event_obj}
    if request.user.is_authenticated:
        if request.user.profile.role=='admin' or request.user.profile.role=='photographer':
            return render(request,'event/view_event_photos_admin.html',context)    
    return render(request,'event/eventdetails1.html',context)

@login_required(login_url='user-login')
def delete_event_photo(request,pk):
    if request.user.profile.role=='admin' or request.user.profile.role=='photographer':
        event_photo_obj=EventPhotos.objects.get(id=pk)
        event_photo_obj.delete()
        messages.success(request,'Photo deleted Successfully!')
        return redirect('view_event_photos',pk=event_photo_obj.event.id)
    else:
        messages.error(request,"You are not authorised!")
        return redirect('home')

# @login_required(login_url='user-login')
# def update_event_photo(request,pk):
#     if request.user.profile.role=='admin' or request.user.profile.role=='photographer':
#         event_photo_object=EventPhotos.objects.get(id=pk)
#         form=EventPhotoForm(instance=event_photo_object)
#         context={'form':form}
#         if request.method=='POST':
#             form=EventPhotoForm(request.POST,request.FILES)
#             if form.is_valid():
#                 event_photo=form.save(commit=False)
#                 print(event_photo_object.event.id)
#                 event_photo.save()
#                 messages.success(request,"Photo Updated Successfully!")
#                 return redirect('view_event_photos',pk=event_photo_object.event.id)
#             else:
#                 messages.error(request,"Couldn't able to update Image")
            
#         return render(request,'event/update_event_photo.html',context)
            
#     else:
#         messages.error(request,"You are not authorised!")
#         return redirect('home')

def update_event_photo(request,pk):
    if request.user.profile.role=='admin' or request.user.profile.role=='photographer':
        event_photo_object=EventPhotos.objects.get(id=pk)
        form=EventPhotoForm(instance=event_photo_object)
        if request.method=='POST':
            form=EventPhotoForm(request.POST,request.FILES,instance=event_photo_object)
            if form.is_valid():
                form.save()
                messages.success(request,"Photo updated successfully!")
                return redirect('view_event_photos',pk=event_photo_object.event.id)
            else:
                pass
        context={'form':form}
        return render(request,'event/update_event_photo.html',context)
    else:
        messages.error(request,"You are not authorised!")
        return redirect('home')

