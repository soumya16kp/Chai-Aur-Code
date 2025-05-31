from django.urls import path,include
from . import views 

urlpatterns = [
    path('signup/',views.signup_view,name='Signup'),
    path('login/',views.login_view,name='Login'),
    path('logout/',views.logout_view,name='Logout'),
    path('Edit_profile/',views.edit_profile,name='edit_profile')
]
