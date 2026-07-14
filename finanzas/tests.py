# finanzas/tests.py
from django.test import TestCase, Client
from django.urls import reverse

class ResultadosViewTests(TestCase):
    def setUp(self):
        # El cliente simula el navegador del usuario
        self.client = Client()
        self.url = reverse('resultados_view')

    def test_calcular_saldo_con_porcentajes_estandar(self):
        """
        Prueba que si enviamos solo el saldo, use los porcentajes estándar 
        (40% Esencial, 15% Estabilidad, 15% Disfrute, 30% Inversión)
        """
        datos_formulario = {
            'saldo': '1000000' # $1.000.000 COP
        }
        
        # 1. Enviamos el POST
        response = self.client.post(self.url, datos_formulario)
        
        # 2. Verificamos que haga la redirección (status 302)
        self.assertEqual(response.status_code, 302)
        
        # 3. Seguimos la redirección (GET) para ver la página final con los resultados
        response_final = self.client.get(self.url)
        
        # 4. Comprobamos que en el contexto existan los datos procesados
        self.assertIn('porcentajes', response_final.context)
        self.assertIn('saldo_total_cop', response_final.context)
        
        # 5. Verificamos que los cálculos estándar sean correctos
        porcentajes = response_final.context['porcentajes']
        # El formato depende de cómo lo devuelva tu utils.py (aquí suponemos que devuelve el string formateado)
        self.assertIn('Esencial (40%)', porcentajes)
        self.assertIn('Inversión (30%)', porcentajes)

    def test_calcular_saldo_con_porcentajes_personalizados(self):
        """
        Prueba que si enviamos porcentajes personalizados en el formulario,
        el sistema calcule usando esos nuevos valores (ej. 50%, 10%, 10%, 30%)
        """
        datos_formulario = {
            'saldo': '1000000',
            'porcentaje_disfrute': '10',     # 10%
            'porcentaje_esencial': '50',     # 50%
            'porcentaje_estabilidad': '10',  # 10%
            'porcentaje_inversion': '30'     # 30%
        }
        
        # 1. Enviamos el POST con el mapa de porcentajes
        response = self.client.post(self.url, datos_formulario)
        self.assertEqual(response.status_code, 302)
        
        # 2. Seguimos al GET
        response_final = self.client.get(self.url)
        
        # 3. Verificamos que el cálculo se haya hecho con los nuevos porcentajes
        porcentajes = response_final.context['porcentajes']
        
        # Le añadimos el .0 a cada porcentaje para que coincida con el float de Python
        self.assertIn('Esencial (50.0%)', porcentajes)
        self.assertIn('Disfrute (10.0%)', porcentajes)
        self.assertIn('Estabilidad (10.0%)', porcentajes)
        self.assertIn('Inversión (30.0%)', porcentajes)
        
    def test_evita_calculo_si_valores_son_invalidos(self):
        """
        Prueba que si mandamos texto en el saldo, no se rompa la app (ValueErrors controlados)
        """
        datos_formulario = {
            'saldo': 'texto_invalido_no_numero'
        }
        response = self.client.post(self.url, datos_formulario)
        self.assertEqual(response.status_code, 302)
        
        response_final = self.client.get(self.url)
        # No debería haber porcentajes calculados en el contexto
        self.assertNotIn('porcentajes', response_final.context)