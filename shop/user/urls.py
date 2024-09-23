from user import views
from django.urls import path


urlpatterns = [
    path("", views.user_index, name="user_index"),
    path("user/<int:id>/", views.user_info, name="user_by_id"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
