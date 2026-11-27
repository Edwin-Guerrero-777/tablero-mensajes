from datetime import datetime, timezone

from django.test import TestCase
from django.urls import reverse

from .models import Mensaje


class PruebasMensaje(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mensaje = Mensaje.objects.create(texto="Esta es una prueba.")

    def test_contenido_modelo(self):
        self.assertEqual(self.mensaje.texto, "Esta es una prueba.")

    def test_str_modelo(self):
        self.assertEqual(str(self.mensaje), "Esta es una prueba.")

    def test_url_existe_en_ubicacion_correcta(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)

    def test_pagina_inicio(self):
        respuesta = self.client.get(reverse("inicio"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "inicio.html")
        self.assertContains(respuesta, "Esta es una prueba.")

    def test_contador_de_mensajes(self):
        respuesta = self.client.get(reverse("inicio"))
        self.assertContains(respuesta, "Total de mensajes: 1")

    def test_fecha_con_formato(self):
        # 23:55 UTC es 17:55 en la Ciudad de México (UTC-6).
        Mensaje.objects.filter(pk=self.mensaje.pk).update(
            fecha=datetime(2026, 10, 10, 23, 55, tzinfo=timezone.utc)
        )
        respuesta = self.client.get(reverse("inicio"))
        self.assertContains(respuesta, "10 de Octubre, 17:55")


class PruebasTableroVacio(TestCase):
    def test_pagina_sin_mensajes(self):
        respuesta = self.client.get(reverse("inicio"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Todavía no hay mensajes.")
        self.assertContains(respuesta, "Total de mensajes: 0")
