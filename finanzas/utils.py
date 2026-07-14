# finanzas/utils.py
import datetime as dt

def formato_cop(valor):
    """Convierte un número al formato de moneda COP: $1.000"""
    return f"${valor:,.0f}".replace(",", ".")

def calcular_porcentaje(total, mapa_porcentajes=None):
    """Calcula los montos basados en el saldo total y un mapa opcional de porcentajes"""
    if total == 0:
        return {}

    # Condicional nuevo: Si el mapa está vacío o no se envía, usamos los de siempre
    if not mapa_porcentajes:
        p_esencial = 40
        p_estabilidad = 15
        p_disfrute = 15
        p_inversion = 30
    else:
        # Si el mapa no está vacío, usamos los valores que trajo el nuevo mapa
        p_esencial = mapa_porcentajes.get("esencial", 40)
        p_estabilidad = mapa_porcentajes.get("estabilidad", 15)
        p_disfrute = mapa_porcentajes.get("disfrute", 15)
        p_inversion = mapa_porcentajes.get("inversion", 30)

    # Convertimos los porcentajes enteros a decimales para la matemática
    esencial = (p_esencial / 100) * total
    estabilidad = (p_estabilidad / 100) * total
    disfrute = (p_disfrute / 100) * total
    inversion = (p_inversion / 100) * total

    return {
        f"Esencial ({p_esencial}%)": esencial,
        f"Estabilidad ({p_estabilidad}%)": estabilidad,
        f"Disfrute ({p_disfrute}%)": disfrute,
        f"Inversión ({p_inversion}%)": inversion
    }

def obtener_datos_procesados(saldo_total, mapa_porcentajes=None):
    """
    Une la lógica de cálculo y formateo en un diccionario listo para Django.
    Recibe el mapa opcional para pasárselo a calcular_porcentaje.
    """
    fecha_actual = dt.datetime.now().strftime("%d/%m/%Y")
    
    # 1. Calculamos los porcentajes pasando el mapa recibido
    porcentajes_raw = calcular_porcentaje(saldo_total, mapa_porcentajes)
    
    # 2. Formateamos los porcentajes a formato COP para la vista
    porcentajes_formateados = {k: formato_cop(v) for k, v in porcentajes_raw.items()}
    
    # 3. Estructuramos el resultado final que irá al HTML
    resultado = {
        "fecha": fecha_actual,
        "saldo_original": saldo_total,
        "saldo_total_cop": formato_cop(saldo_total),
        "porcentajes": porcentajes_formateados  
    }
    
    return resultado