from django.urls import path
from . import views

urlpatterns = [
    path('hire_us/', views.hire_us,name='hire_us'),
    path('phase_allocation/<str:pk>/',views.event_phase_allocation,name='event_phase_allocation'),
    path('events_list/<str:event_list_type>/',views.admin_events_list,name='admin_events_list'),
    path('events_list/',views.view_events_list_by_user,name='user_events_list'),
    path('approve_event/<str:pk>/',views.approve_event,name='approve_event'),
    path('reject_event/<str:pk>/',views.reject_event,name='reject_event'),
    path('assign_photographers/<str:pk>/',views.assign_photographers,name='assign_photographers'),
    path('upload_event_photos/<str:pk>/',views.upload_event_photos,name='upload_event_photos'),
    path('view_event_photos/<str:pk>/',views.view_event_photos,name='view_event_photos'),
    path('delete_event_photo/<str:pk>/',views.delete_event_photo,name='delete_event_photo'),
    path('update_event_photo/<str:pk>/',views.update_event_photo,name='update_event_photo')
]