from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('dash/', views.dash_view, name='dash'),
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('signup/', views.signup_view, name='signup'),

]
