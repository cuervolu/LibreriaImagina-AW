from django.urls import path
from libreria_imagina.views import * 

app_name = 'auth'

urlpatterns = [
    path('login/',login_view, name='login'),
    path('signup/',signup_view, name='signup'),
]
