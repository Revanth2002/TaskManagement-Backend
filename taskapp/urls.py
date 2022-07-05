from django.urls import path,include
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('adminregister/',AdminRegisterView.as_view(), name='adminregister'),
    path('adminlogin/',AdminLoginView.as_view(), name='adminlogin'),

    path('task/', TaskView.as_view(), name='task'),
    path('search/',SearchTask.as_view(), name='search'),

    path('admintask/',AdminTaskView.as_view(), name='admintask'),
    path('adminusers/',AdminViewUserView.as_view(), name='adminusers'),

]