from django.urls import path
from . import views

urlpatterns = [
    path('', views.cv_upload_view, name='cv_check'),
]
