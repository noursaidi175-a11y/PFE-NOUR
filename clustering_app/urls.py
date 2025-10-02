from django.urls import path
from . import views

urlpatterns = [
    path('', views.clustering_view, name='employee_clustering'),
]
