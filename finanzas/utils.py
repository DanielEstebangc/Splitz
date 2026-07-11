# finanzas/utils.py
import datetime as dt

def formato_cop(valor):
    """Convierte un número al formato de moneda COP: $1.000"""
    return f"${valor:,.0f}".replace(",", ".")

def calcular_porcentaje(total):
    """Calcula los montos fijos basados en el saldo total"""
    if total == 0:
        return {}

    esencial = 0.40 * total
    estabilidad = 0.15 * total
    disfrute = 0.15 * total
    inversion = 0.30 * total

    return {
        "Esencial (40%)": esencial,
        "Estabilidad (15%)": estabilidad,
        "Disfrute (15%)": disfrute,
        "Inversión (30%)": inversion
    }

def obtener_datos_procesados(saldo_total):
    """
    Reemplaza a convercion_data. 
    Une la lógica de cálculo y formateo en un diccionario listo para Django.
    """
    fecha_actual = dt.datetime.now().strftime("%d/%m/%Y")
    
    # 1. Calculamos los porcentajes (valores numéricos)
    porcentajes_raw = calcular_porcentaje(saldo_total)
    
    # 2. Formateamos los porcentajes a formato COP para la vista
    porcentajes_formateados = {k: formato_cop(v) for k, v in porcentajes_raw.items()}
    
    # 3. Estructuramos el resultado final que irá al HTML
    resultado = {
        "fecha": fecha_actual,
        "saldo_original": saldo_total,
        "saldo_total_cop": formato_cop(saldo_total),
        "porcentajes": porcentajes_formateados  # Diccionario listo para iterar en el HTML
    }
    
    return resultado