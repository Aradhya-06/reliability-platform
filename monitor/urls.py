from django.urls import path
from .views import *

urlpatterns=[
    path("",dashboard,name="dashboard"),
    path("dashboard/",dashboard,name="dashboard"),
    path('health/', health_check, name='health'),
    path('add_monitor/', add_monitor, name='add_monitor'),
    path('monitor/<int:monitor_id>/', monitor_detail, name='monitor_detail'),
    path('monitor/<int:monitor_id>/delete/', delete_monitor, name='delete_monitor'),
    path('monitor/<int:monitor_id>/toggle/', toggle_monitor, name='toggle_monitor'),
]