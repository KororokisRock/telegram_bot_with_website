
from django.urls import path
from . import views as v

urlpatterns = [
    path('/login',v.login , name='login'),
    path('/registr/', v.reg, name='reg'),
]