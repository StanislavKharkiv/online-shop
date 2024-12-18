from django.urls import path
from product import views


urlpatterns = [
    path("", views.ProductListView.as_view(), name="products"),
    path("create/", views.CreateProductView.as_view(), name="create_product"),
    path("<int:product_id>/", views.DetailProductView.as_view(), name="product_detail"),
    path("<int:product_id>/edit", views.EditProductView.as_view(), name="product_edit"),
]
