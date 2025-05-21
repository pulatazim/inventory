from django.urls import path
from .views import MaterialCalculationApiView

urlpatterns = [
    path('calculate-materials/', MaterialCalculationApiView.as_view(), name='material_calculation'),
]