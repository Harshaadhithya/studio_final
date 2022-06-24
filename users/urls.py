from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.user_login,name='user-login'),
    path('logout/',views.user_logour,name='logout'),
    path('photographer_signup/',views.photographer_signup,name='photographer_signup'),

    # path('user_home/',views.user_home,name='user-home'),
    
]