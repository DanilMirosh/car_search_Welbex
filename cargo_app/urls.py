from django.urls import path
from .views import (
    LocationListCreateView,
    CarListCreateView,
    CargoListCreateView,
    CargoRetrieveUpdateDestroyView,
    CargoFilterListView,
    CarLocationUpdateView,
)

urlpatterns = [
    path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('car/', CarListCreateView.as_view(), name='machine-list-create'),
    path('cargos/', CargoListCreateView.as_view(), name='cargo-list-create'),
    path('cargos/<int:pk>/', CargoRetrieveUpdateDestroyView.as_view(), name='cargo-retrieve-update-destroy'),
    path('cargos/filter/', CargoFilterListView.as_view(), name='cargo-filter-list'),
    path('car/<int:pk>/update-location/', CarLocationUpdateView.as_view(), name='car-update-location'),
]
