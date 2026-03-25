import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import AfluenciaMetro, AfluenciaMetrobus, AfluenciaSTE, AfluenciaRTP

TODAY = datetime.date(2024, 1, 15)


def _metro(ckan_id=1, source=AfluenciaMetro.SIMPLE, linea="Linea 1", estacion="Zaragoza", **kw):
    return AfluenciaMetro.objects.create(
        ckan_id=ckan_id, source=source, linea=linea, estacion=estacion,
        fecha=TODAY, anio=2024, mes="Enero", afluencia=20000, **kw
    )


def _metrobus(ckan_id=1, source=AfluenciaMetrobus.SIMPLE, linea="Línea 1", **kw):
    return AfluenciaMetrobus.objects.create(
        ckan_id=ckan_id, source=source, linea=linea,
        fecha=TODAY, anio=2024, mes="Enero", afluencia=5000, **kw
    )


def _ste(ckan_id=1, sistema=AfluenciaSTE.CABLEBUS, **kw):
    return AfluenciaSTE.objects.create(
        ckan_id=ckan_id, sistema=sistema, tipo_pago="Prepago",
        fecha=TODAY, anio=2024, mes="Enero", afluencia=1000, **kw
    )


class AfluenciaMetroModelTest(TestCase):
    def test_str(self):
        m = _metro()
        assert "Linea 1" in str(m)
        assert "Zaragoza" in str(m)

    def test_unique_together_ckan_id_source(self):
        from django.db import IntegrityError
        _metro(ckan_id=1, source=AfluenciaMetro.SIMPLE)
        with self.assertRaises(IntegrityError):
            _metro(ckan_id=1, source=AfluenciaMetro.SIMPLE)

    def test_same_ckan_id_different_source_allowed(self):
        _metro(ckan_id=1, source=AfluenciaMetro.SIMPLE)
        _metro(ckan_id=1, source=AfluenciaMetro.DESGLOSADA)
        assert AfluenciaMetro.objects.count() == 2


class AfluenciaMetroAPITest(APITestCase):
    def setUp(self):
        _metro(ckan_id=1, linea="Linea 1", estacion="Zaragoza")
        _metro(ckan_id=2, linea="Linea 2", estacion="Portales", source=AfluenciaMetro.DESGLOSADA)

    def test_list(self):
        url = reverse("metro-list")
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 2

    def test_filter_by_linea(self):
        url = reverse("metro-list") + "?linea=Linea+1"
        resp = self.client.get(url)
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["estacion"] == "Zaragoza"

    def test_filter_by_source(self):
        url = reverse("metro-list") + "?source=desglosada"
        resp = self.client.get(url)
        assert resp.data["count"] == 1

    def test_read_only(self):
        url = reverse("metro-list")
        assert self.client.post(url, {}).status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class AfluenciaSTEModelTest(TestCase):
    def test_sistema_display(self):
        s = _ste(sistema=AfluenciaSTE.TREN_LIGERO)
        assert s.get_sistema_display() == "Tren Ligero"

    def test_unique_together_ckan_id_sistema(self):
        from django.db import IntegrityError
        _ste(ckan_id=1, sistema=AfluenciaSTE.CABLEBUS)
        with self.assertRaises(IntegrityError):
            _ste(ckan_id=1, sistema=AfluenciaSTE.CABLEBUS)

    def test_same_ckan_id_different_sistema_allowed(self):
        _ste(ckan_id=1, sistema=AfluenciaSTE.CABLEBUS)
        _ste(ckan_id=1, sistema=AfluenciaSTE.TROLEBUS)
        assert AfluenciaSTE.objects.count() == 2


class AfluenciaSTEAPITest(APITestCase):
    def setUp(self):
        _ste(ckan_id=1, sistema=AfluenciaSTE.CABLEBUS)
        _ste(ckan_id=2, sistema=AfluenciaSTE.TROLEBUS)
        _ste(ckan_id=3, sistema=AfluenciaSTE.TREN_LIGERO)

    def test_list_all(self):
        url = reverse("ste-list")
        resp = self.client.get(url)
        assert resp.data["count"] == 3

    def test_filter_by_sistema(self):
        url = reverse("ste-list") + "?sistema=cablebus"
        resp = self.client.get(url)
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["sistema"] == "cablebus"

    def test_response_includes_sistema_display(self):
        url = reverse("ste-list") + "?sistema=tren_ligero"
        resp = self.client.get(url)
        assert resp.data["results"][0]["sistema_display"] == "Tren Ligero"
