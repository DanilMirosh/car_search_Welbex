from django.urls import path
from cargo_app.views import CargoListCreateView, CarListCreateView


urlpatterns = [
    path('cargos/', CargoListCreateView.as_view(), name='cargo-list-create'),
    path('cars/', CarListCreateView.as_view(), name='car-list-create'),
]
