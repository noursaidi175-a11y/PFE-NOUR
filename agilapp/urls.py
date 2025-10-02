from django.urls import path
from . import views

urlpatterns = [
    path('', views.form_predict_turnover, name='form_predict_turnover'),
    
]
