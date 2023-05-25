from django.urls import path
from cargo_app.views import CargoListCreateView, CargoDetailView, CarListCreateView, CarDetailView


urlpatterns = [
    path('cargos/', CargoListCreateView.as_view(), name='cargo-list-create'),
    path('cargos/<int:pk>/', CargoDetailView.as_view(), name='cargo-detail'),
    path('cars/', CarListCreateView.as_view(), name='car-list-create'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car-detail'),
]
