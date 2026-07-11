# finanzas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Esto significa que la vista 'resultados_view' responderá en la raíz de esta app
    path('', views.resultados_view, name='resultados'),
]