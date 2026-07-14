# finanzas/views.py
from django.shortcuts import render, redirect
from .utils import obtener_datos_procesados

def resultados_view(request):
    contexto = {}
    
    if request.method == "POST":
        # Recibimos el saldo desde el formulario HTML
        saldo_input = request.POST.get("saldo")
        
        # 1. 📥 Intentamos capturar los porcentajes desde el formulario
        disfrute_input = request.POST.get("porcentaje_disfrute")
        esencial_input = request.POST.get("porcentaje_esencial")
        estabilidad_input = request.POST.get("porcentaje_estabilidad")
        inversion_input = request.POST.get("porcentaje_inversion")
        
        # 2. 🗺️ Si el usuario envió los porcentajes, armamos el mapa. Si no, queda en None
        mapa_porcentajes = None
        if disfrute_input and esencial_input and estabilidad_input and inversion_input:
            try:
                mapa_porcentajes = {
                    "disfrute": float(disfrute_input),      
                    "esencial": float(esencial_input),      
                    "estabilidad": float(estabilidad_input), 
                    "inversion": float(inversion_input)      
                }
            except ValueError:
                mapa_porcentajes = None

        if saldo_input:
            try:
                saldo_total = float(saldo_input)
                
                # 3. 🚀 Pasamos el saldo y el mapa (que puede ser el diccionario o None)
                datos_calculados = obtener_datos_procesados(saldo_total, mapa_porcentajes)
                
                # 4. 🔥 GUARDAMOS LOS PORCENTAJES EN LOS RESULTADOS TEMPORALES
                # Si el usuario editó los porcentajes, se los pasamos al diccionario de resultados
                # para que viajen seguros en la sesión y no sufran de amnesia tras el redirect.
                if mapa_porcentajes:
                    datos_calculados['porcentaje_disfrute'] = disfrute_input
                    datos_calculados['porcentaje_esencial'] = esencial_input
                    datos_calculados['porcentaje_estabilidad'] = estabilidad_input
                    datos_calculados['porcentaje_inversion'] = inversion_input

                # Guardamos la versión gorda con los porcentajes incluidos en la sesión
                request.session['resultados_temporales'] = datos_calculados
            except ValueError:
                pass # Por si envían algo que no es un número
            
        # REDIRECCIÓN CLAVE: Limpia la petición POST y evita el error 404 de Render
        return redirect('resultados_view')
        
    # Si la petición es GET (carga inicial o después de redirigir)
    # Sacamos los datos de la sesión si existen
    contexto = request.session.pop('resultados_temporales', {})
    
    return render(request, "finanzas/resultados.html", contexto)