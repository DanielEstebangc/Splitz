# finanzas/views.py
from django.shortcuts import render
from .utils import obtener_datos_procesados

def resultados_view(request):
    contexto = {}
    
    if request.method == "POST":
        # Recibimos el saldo desde el formulario HTML
        saldo_input = request.POST.get("saldo")
        
        if saldo_input:
            saldo_total = float(saldo_input)
            # Ejecutamos tu lógica unificada
            contexto = obtener_datos_procesados(saldo_total)
            
    return render(request, "finanzas/resultados.html", contexto)