from django.urls import path

from . import views

urlpatterns = [
    path('startups', views.startup_index, name='startup_index'),
    path('startups/<int:id>', views.startup_show, name='startup_show'),
]
