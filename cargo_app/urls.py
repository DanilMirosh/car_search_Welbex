from django.urls import path
from .views import (
    LocationListView, CarListView, CarRetrieveUpdateDestroyView,
    CargoListCreateView, CargoRetrieveUpdateDestroyView,
    CargoCarListCreateView, CargoCarRetrieveUpdateDestroyView,
    CarLocationUpdateView
)

urlpatterns = [
    path('locations/', LocationListView.as_view(), name='location-list'),
    path('cars/', CarListView.as_view(), name='car-list'),
    path('cars/<int:pk>/', CarRetrieveUpdateDestroyView.as_view(), name='car-detail'),
    path('cargos/', CargoListCreateView.as_view(), name='cargo-list'),
    path('cargos/<int:pk>/', CargoRetrieveUpdateDestroyView.as_view(), name='cargo-detail'),
    path('cargocars/', CargoCarListCreateView.as_view(), name='cargocar-list'),
    path('cargocars/<int:pk>/', CargoCarRetrieveUpdateDestroyView.as_view(), name='cargocar-detail'),
    path('cars/<int:pk>/update_location/', CarLocationUpdateView.as_view(), name='car-update-location'),
]
