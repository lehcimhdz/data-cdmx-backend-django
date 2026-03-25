from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import RiesgoInundacion, Refugio


def _inundacion(ckan_id=1, alcaldia="Xochimilco", intensidad="Bajo", **kw):
    return RiesgoInundacion.objects.create(
        ckan_id=ckan_id, alcaldia=alcaldia, intensidad=intensidad,
        taxonomia="Inundaciones", fenomeno="Hidrometeorologicos",
        r_p_v_e="Peligro", cvegeo="0901300011154", entidad="Ciudad de México", **kw
    )


def _refugio(ckan_id=1, nombre="Peñoles", delegacion="Cuauhtémoc", **kw):
    return Refugio.objects.create(
        ckan_id=ckan_id, nombre=nombre, delegacion=delegacion,
        cap_albergue=100, region="Centro", **kw
    )


class RiesgoInundacionModelTest(TestCase):
    def test_str(self):
        r = _inundacion()
        assert "Inundaciones" in str(r)
        assert "Xochimilco" in str(r)

    def test_ckan_id_unique(self):
        from django.db import IntegrityError
        _inundacion(ckan_id=1)
        with self.assertRaises(IntegrityError):
            _inundacion(ckan_id=1)


class RiesgoInundacionAPITest(APITestCase):
    def setUp(self):
        _inundacion(ckan_id=1, alcaldia="Xochimilco", intensidad="Bajo")
        _inundacion(ckan_id=2, alcaldia="Iztapalapa", intensidad="Alto")
        _inundacion(ckan_id=3, alcaldia="Xochimilco", intensidad="Medio")

    def test_list_all(self):
        url = reverse("inundacion-list")
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 3

    def test_filter_by_alcaldia(self):
        url = reverse("inundacion-list") + "?alcaldia=Xochimilco"
        resp = self.client.get(url)
        assert resp.data["count"] == 2

    def test_filter_by_intensidad(self):
        url = reverse("inundacion-list") + "?intensidad=Alto"
        resp = self.client.get(url)
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["alcaldia"] == "Iztapalapa"


class RefugioModelTest(TestCase):
    def test_str(self):
        r = _refugio()
        assert "Peñoles" in str(r)

    def test_ckan_id_unique(self):
        from django.db import IntegrityError
        _refugio(ckan_id=1)
        with self.assertRaises(IntegrityError):
            _refugio(ckan_id=1)


class RefugioAPITest(APITestCase):
    def setUp(self):
        _refugio(ckan_id=1, nombre="Peñoles", delegacion="Cuauhtémoc")
        _refugio(ckan_id=2, nombre="Deportivo Sur", delegacion="Iztapalapa")

    def test_list_all(self):
        url = reverse("refugio-list")
        resp = self.client.get(url)
        assert resp.data["count"] == 2

    def test_filter_by_delegacion(self):
        url = reverse("refugio-list") + "?delegacion=Iztapalapa"
        resp = self.client.get(url)
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["nombre"] == "Deportivo Sur"

    def test_search_by_nombre(self):
        url = reverse("refugio-list") + "?search=Peñoles"
        resp = self.client.get(url)
        assert resp.data["count"] == 1
