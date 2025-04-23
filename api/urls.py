from django.urls import path
from api.views.shop import (
    ProductCreateView,
    ProductListView,
    ProductRetrieveUpdateDestroyView
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
]