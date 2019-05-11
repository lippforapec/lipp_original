from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('startups', views.startup_index, name='startup_index'),
    path('startups/<int:id>', views.startup_show, name='startup_show'),
    path('startups/<int:id>/edit', views.startup_edit, name='startup_edit'),
    path('startups/new', views.startup_new, name='startup_new'),
    path('startups/search_results', views.startup_search_results, name='startup_search_results'),
    
    
]
