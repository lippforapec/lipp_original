from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # startups
    path('', views.main, name='home'),
    path('startups', views.startup_index, name='startup_index'),
    path('startups/<int:id>', views.startup_show, name='startup_show'),
    path('startups/<int:id>/edit', views.startup_edit, name='startup_edit'),
    path('startups/new', views.startup_new, name='startup_new'),

    # accounts
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.register, name='signup'),
    path('accounts/usertype/', views.get_user_type, name='usertype'),

    # likes
    path('likes/create', views.like_create, name='create_like'),
    path('likes/delete/<int:startup_id>', views.like_delete, name='delete_like'),
    #path('like/<int:id>', views.DeleteLike.as_view(), name='delete_like')

    # feedbacks
    path('feedback/create', views.feedback_create, name='create_feedback'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
