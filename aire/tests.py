import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Estacion, Lectura
from .tasks import _calcular_indice_calidad_aire


def _estacion(ckan_id=1, id_estacion="BJU", alcaldia="Benito Juárez", **kw):
    return Estacion.objects.create(
        ckan_id=ckan_id,
        id_estacion=id_estacion,
        nombre=f"Estación {id_estacion}",
        alcaldia=alcaldia,
        latitud=19.37,
        longitud=-99.15,
        **kw,
    )


def _lectura(ckan_id=1, estacion=None, contaminante="PM2.5", valor=35.2,
             fecha=None, hora=12, **kw):
    return Lectura.objects.create(
        ckan_id=ckan_id,
        estacion=estacion,
        contaminante=contaminante,
        valor=valor,
        unidad="µg/m³",
        fecha=fecha or datetime.date(2024, 3, 1),
        hora=hora,
        **kw,
    )


# ── Model tests ──────────────────────────────────────────────────────────────

class EstacionModelTest(TestCase):
    def test_str(self):
        e = _estacion()
        assert "BJU" in str(e)
        assert "Benito Juárez" in str(e)

    def test_ckan_id_unique(self):
        from django.db import IntegrityError
        _estacion(ckan_id=1)
        with self.assertRaises(IntegrityError):
            _estacion(ckan_id=1, id_estacion="MER")

    def test_id_estacion_unique(self):
        from django.db import IntegrityError
        _estacion(ckan_id=1, id_estacion="BJU")
        with self.assertRaises(IntegrityError):
            _estacion(ckan_id=2, id_estacion="BJU")


class LecturaModelTest(TestCase):
    def setUp(self):
        self.estacion = _estacion()

    def test_str(self):
        l = _lectura(estacion=self.estacion)
        assert "PM2.5" in str(l)
        assert "BJU" in str(l)

    def test_ckan_id_unique(self):
        from django.db import IntegrityError
        _lectura(ckan_id=1, estacion=self.estacion)
        with self.assertRaises(IntegrityError):
            _lectura(ckan_id=1, estacion=self.estacion, contaminante="O3")


# ── API tests — Estacion ──────────────────────────────────────────────────────

class EstacionAPITest(APITestCase):
    def setUp(self):
        _estacion(ckan_id=1, id_estacion="BJU", alcaldia="Benito Juárez")
        _estacion(ckan_id=2, id_estacion="MER", alcaldia="Venustiano Carranza")
        _estacion(ckan_id=3, id_estacion="PED", alcaldia="Benito Juárez")

    def test_list_all(self):
        url = reverse("aire-estacion-list")
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 3

    def test_filter_by_alcaldia(self):
        url = reverse("aire-estacion-list") + "?alcaldia=Benito Juárez"
        resp = self.client.get(url)
        assert resp.data["count"] == 2

    def test_search_by_id_estacion(self):
        url = reverse("aire-estacion-list") + "?search=MER"
        resp = self.client.get(url)
        assert resp.data["count"] == 1

    def test_retrieve(self):
        e = Estacion.objects.first()
        url = reverse("aire-estacion-detail", args=[e.pk])
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["id_estacion"] == e.id_estacion

    def test_read_only(self):
        url = reverse("aire-estacion-list")
        resp = self.client.post(url, {})
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


# ── API tests — Lectura ───────────────────────────────────────────────────────

class LecturaAPITest(APITestCase):
    def setUp(self):
        self.bju = _estacion(ckan_id=1, id_estacion="BJU", alcaldia="Benito Juárez")
        self.mer = _estacion(ckan_id=2, id_estacion="MER", alcaldia="Venustiano Carranza")
        _lectura(ckan_id=1, estacion=self.bju, contaminante="PM2.5", valor=35.2,
                 fecha=datetime.date(2024, 3, 1))
        _lectura(ckan_id=2, estacion=self.bju, contaminante="O3", valor=80.0,
                 fecha=datetime.date(2024, 3, 1))
        _lectura(ckan_id=3, estacion=self.mer, contaminante="PM2.5", valor=45.1,
                 fecha=datetime.date(2024, 3, 2))

    def test_list_all(self):
        url = reverse("aire-lectura-list")
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 3

    def test_filter_by_contaminante(self):
        url = reverse("aire-lectura-list") + "?contaminante=PM2.5"
        resp = self.client.get(url)
        assert resp.data["count"] == 2

    def test_filter_by_estacion(self):
        url = reverse("aire-lectura-list") + f"?estacion={self.bju.pk}"
        resp = self.client.get(url)
        assert resp.data["count"] == 2

    def test_filter_by_fecha(self):
        url = reverse("aire-lectura-list") + "?fecha=2024-03-02"
        resp = self.client.get(url)
        assert resp.data["count"] == 1

    def test_serializer_includes_estacion_code(self):
        url = reverse("aire-lectura-list") + "?contaminante=O3"
        resp = self.client.get(url)
        assert resp.data["results"][0]["estacion_id_estacion"] == "BJU"


# ── Celery task tests (pure logic) ────────────────────────────────────────────

class CalcularIndiceAireTest(TestCase):
    def setUp(self):
        self.bju = _estacion(ckan_id=1, id_estacion="BJU")
        _lectura(ckan_id=1, estacion=self.bju, contaminante="PM2.5", valor=30.0,
                 fecha=datetime.date(2024, 3, 1))
        _lectura(ckan_id=2, estacion=self.bju, contaminante="PM2.5", valor=40.0,
                 fecha=datetime.date(2024, 3, 1))
        _lectura(ckan_id=3, estacion=self.bju, contaminante="O3", valor=70.0,
                 fecha=datetime.date(2024, 3, 2))

    def test_returns_list(self):
        result = _calcular_indice_calidad_aire()
        assert isinstance(result, list)

    def test_includes_expected_contaminantes(self):
        result = _calcular_indice_calidad_aire()
        contaminantes = {r["contaminante"] for r in result}
        assert "PM2.5" in contaminantes
        assert "O3" in contaminantes

    def test_promedio_pm25(self):
        result = _calcular_indice_calidad_aire()
        pm25 = next(r for r in result if r["contaminante"] == "PM2.5")
        assert pm25["promedio"] == 35.0  # (30 + 40) / 2
