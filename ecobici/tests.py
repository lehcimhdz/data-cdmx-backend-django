import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CicloEstacion, ViajesDiarios, ViajesDesglosados


def _estacion(ckan_id=1, alcaldia="Cuauhtémoc", estatus="AC", **kw):
    return CicloEstacion.objects.create(
        ckan_id=ckan_id,
        alcaldia=alcaldia,
        estatus=estatus,
        num_cicloe=f"CE-{ckan_id:03d}",
        calle_prin="Reforma",
        colonia="Juárez",
        sistema="ECOBICI",
        **kw,
    )


def _viaje_diario(ckan_id=1, fecha=None, genero="M", viajes=100, anio=2024, mes=3, **kw):
    return ViajesDiarios.objects.create(
        ckan_id=ckan_id,
        fecha=fecha or datetime.date(2024, 3, 1),
        genero=genero,
        viajes=viajes,
        anio=anio,
        mes=mes,
        **kw,
    )


def _viaje_desglosado(ckan_id=1, genero="M", rango_edad="26-35", hora=8, **kw):
    return ViajesDesglosados.objects.create(
        ckan_id=ckan_id,
        fecha_corte=datetime.date(2024, 3, 1),
        genero=genero,
        rango_edad=rango_edad,
        hora=hora,
        viajes=50,
        anio=2024,
        mes=3,
        **kw,
    )


# ── Model tests ──────────────────────────────────────────────────────────────

class CicloEstacionModelTest(TestCase):
    def test_str(self):
        e = _estacion()
        assert "CE-001" in str(e)
        assert "Reforma" in str(e)
        assert "Cuauhtémoc" in str(e)

    def test_ckan_id_unique(self):
        from django.db import IntegrityError
        _estacion(ckan_id=1)
        with self.assertRaises(IntegrityError):
            _estacion(ckan_id=1)


class ViajesDiariosModelTest(TestCase):
    def test_str(self):
        v = _viaje_diario()
        assert "2024-03-01" in str(v)
        assert "100" in str(v)

    def test_ckan_id_unique(self):
        from django.db import IntegrityError
        _viaje_diario(ckan_id=1)
        with self.assertRaises(IntegrityError):
            _viaje_diario(ckan_id=1)


class ViajesDesglosadosModelTest(TestCase):
    def test_str(self):
        v = _viaje_desglosado()
        assert "26-35" in str(v)
        assert "8" in str(v)

    def test_ckan_id_unique(self):
        from django.db import IntegrityError
        _viaje_desglosado(ckan_id=1)
        with self.assertRaises(IntegrityError):
            _viaje_desglosado(ckan_id=1)


# ── API tests — CicloEstacion ─────────────────────────────────────────────────

class CicloEstacionAPITest(APITestCase):
    def setUp(self):
        _estacion(ckan_id=1, alcaldia="Cuauhtémoc", estatus="AC")
        _estacion(ckan_id=2, alcaldia="Iztapalapa", estatus="AC")
        _estacion(ckan_id=3, alcaldia="Cuauhtémoc", estatus="IN")

    def test_list_all(self):
        url = reverse("cicloestacion-list")
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 3

    def test_filter_by_alcaldia(self):
        url = reverse("cicloestacion-list") + "?alcaldia=Cuauhtémoc"
        resp = self.client.get(url)
        assert resp.data["count"] == 2

    def test_filter_by_estatus(self):
        url = reverse("cicloestacion-list") + "?estatus=IN"
        resp = self.client.get(url)
        assert resp.data["count"] == 1

    def test_retrieve(self):
        e = CicloEstacion.objects.first()
        url = reverse("cicloestacion-detail", args=[e.pk])
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["ckan_id"] == e.ckan_id

    def test_read_only_post_not_allowed(self):
        url = reverse("cicloestacion-list")
        resp = self.client.post(url, {})
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


# ── API tests — ViajesDiarios ─────────────────────────────────────────────────

class ViajesDiariosAPITest(APITestCase):
    def setUp(self):
        _viaje_diario(ckan_id=1, genero="M", viajes=200, fecha=datetime.date(2024, 3, 1))
        _viaje_diario(ckan_id=2, genero="F", viajes=150, fecha=datetime.date(2024, 3, 1))
        _viaje_diario(ckan_id=3, genero="M", viajes=180, fecha=datetime.date(2024, 4, 1), anio=2024, mes=4)

    def test_list_all(self):
        url = reverse("viajesdiarios-list")
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 3

    def test_filter_by_genero(self):
        url = reverse("viajesdiarios-list") + "?genero=M"
        resp = self.client.get(url)
        assert resp.data["count"] == 2

    def test_filter_by_mes(self):
        url = reverse("viajesdiarios-list") + "?mes=4"
        resp = self.client.get(url)
        assert resp.data["count"] == 1


# ── API tests — ViajesDesglosados ─────────────────────────────────────────────

class ViajesDesglosadosAPITest(APITestCase):
    def setUp(self):
        _viaje_desglosado(ckan_id=1, genero="M", rango_edad="26-35", hora=8)
        _viaje_desglosado(ckan_id=2, genero="F", rango_edad="26-35", hora=9)
        _viaje_desglosado(ckan_id=3, genero="M", rango_edad="36-45", hora=8)

    def test_list_all(self):
        url = reverse("viajesdesglosados-list")
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 3

    def test_filter_by_genero(self):
        url = reverse("viajesdesglosados-list") + "?genero=F"
        resp = self.client.get(url)
        assert resp.data["count"] == 1

    def test_filter_by_rango_edad(self):
        url = reverse("viajesdesglosados-list") + "?rango_edad=26-35"
        resp = self.client.get(url)
        assert resp.data["count"] == 2
