from user import views
from django.urls import path


urlpatterns = [
    path("", views.ProfileView.as_view(), name="user_index"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
