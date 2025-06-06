from django.contrib.auth import views as auth_views
from django.urls import path, include
from members import views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import tinymce_image_upload
from members import views as member_views
from django.shortcuts import redirect


app_name = "members"

urlpatterns = [
    path("", views.member_list, name="member_list"),
    path("badges/", views.badge_board, name="badge_board"),
    path('<int:member_id>/biography/', views.biography_view, name='biography_view'),
    path('tinymce/', include('tinymce.urls')),
    path("<int:member_id>/view/", views.member_view, name="member_view"),
    path('set-password/', views.set_password, name='set_password'),
    path("tinymce-upload/", tinymce_image_upload, name="tinymce_image_upload"),
    path('training-progress/', lambda req: redirect('instructors:member_training_grid', req.user.pk), name='training_progress',


)] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import handler403

handler403 = "django.views.defaults.permission_denied"

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

