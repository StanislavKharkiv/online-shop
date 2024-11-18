from store import views
from django.urls import path


urlpatterns = [
    path("", views.StoreView.as_view(), name="stores"),
    path("create/", views.CreateStoreView.as_view(), name="create_store"),
    path("<int:store_id>/", views.StoreDetailView.as_view(), name="store_detail"),
    path("<str:username>/", views.UserStoresView.as_view(), name="user_stores"),
]
