# finanzas/views.py
from django.shortcuts import render, redirect
from .utils import obtener_datos_procesados

def resultados_view(request):
    contexto = {}
    
    if request.method == "POST":
        # Recibimos el saldo desde el formulario HTML
        saldo_input = request.POST.get("saldo")
        
        if saldo_input:
            try:
                saldo_total = float(saldo_input)
                # Ejecutamos tu lógica unificada
                datos_calculados = obtener_datos_procesados(saldo_total)
                
                # Guardamos los resultados temporalmente en la sesión del navegador
                request.session['resultados_temporales'] = datos_calculados
            except ValueError:
                pass # Por si envían algo que no es un número
            
        # 🚀 REDIRECCIÓN CLAVE: Limpia la petición POST y evita el error 404 de Render
        return redirect('resultados_view')
        
    # Si la petición es GET (carga inicial o después de redirigir)
    # Sacamos los datos de la sesión si existen
    contexto = request.session.pop('resultados_temporales', {})
    
    return render(request, "finanzas/resultados.html", contexto)