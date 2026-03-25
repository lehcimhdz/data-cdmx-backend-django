import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CarpetaInvestigacion

HOY = datetime.date(2018, 6, 15)


def _carpeta(ckan_id=1, delito="ROBO", alcaldia="CUAUHTÉMOC", categoria="DELITO DE ALTO IMPACTO", **kw):
    return CarpetaInvestigacion.objects.create(
        ckan_id=ckan_id, delito=delito, alcaldia_hechos=alcaldia,
        categoria_delito=categoria, fecha_hecho=HOY, ao_hechos="2018",
        mes_hechos="Junio", **kw
    )


class CarpetaModelTest(TestCase):
    def test_str(self):
        c = _carpeta()
        assert "ROBO" in str(c)
        assert "CUAUHTÉMOC" in str(c)

    def test_ckan_id_unique(self):
        from django.db import IntegrityError
        _carpeta(ckan_id=1)
        with self.assertRaises(IntegrityError):
            _carpeta(ckan_id=1)

    def test_nullable_coords(self):
        c = CarpetaInvestigacion.objects.create(ckan_id=99, delito="FRAUDE")
        assert c.latitud is None
        assert c.longitud is None


class CarpetaAPITest(APITestCase):
    def setUp(self):
        _carpeta(ckan_id=1, delito="ROBO", alcaldia="CUAUHTÉMOC", categoria="DELITO DE ALTO IMPACTO")
        _carpeta(ckan_id=2, delito="LESIONES", alcaldia="IZTAPALAPA", categoria="DELITO DE BAJO IMPACTO")
        _carpeta(ckan_id=3, delito="FRAUDE", alcaldia="CUAUHTÉMOC", categoria="DELITO PATRIMONIAL")

    def test_list_all(self):
        url = reverse("carpeta-list")
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 3

    def test_filter_by_alcaldia(self):
        url = reverse("carpeta-list") + "?alcaldia_hechos=CUAUHTÉMOC"
        resp = self.client.get(url)
        assert resp.data["count"] == 2

    def test_filter_by_categoria(self):
        url = reverse("carpeta-list") + "?categoria_delito=DELITO+DE+ALTO+IMPACTO"
        resp = self.client.get(url)
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["delito"] == "ROBO"

    def test_search_by_delito(self):
        url = reverse("carpeta-list") + "?search=LESIONES"
        resp = self.client.get(url)
        assert resp.data["count"] == 1

    def test_read_only(self):
        url = reverse("carpeta-list")
        assert self.client.post(url, {}).status_code == status.HTTP_405_METHOD_NOT_ALLOWED
