from django.urls import path
from .views import *

urlpatterns=[
    #path("",home,name="home"),
    path("",dashboard,name="dashboard"),
    path('health/', health_check, name='health'),
    path('tasks/', get_tasks, name='tasks'),
]