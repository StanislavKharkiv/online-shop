from user import views
from django.urls import path

urlpatterns = [
    path('', views.user_index),
    path('<int:id>/', views.user_info),
]