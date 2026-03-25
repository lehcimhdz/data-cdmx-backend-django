"""
Tests de la app colonias.

Ejecutar:
    python manage.py test colonias
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Colonia


def _make_colonia(**kwargs) -> Colonia:
    defaults = {
        "ckan_id": 1,
        "nombre": "Lomas de Chapultepec",
        "clave": "LC01",
        "cvegeo": "0900000001",
        "cve_dleg": "16",
        "gid": 1,
        "object_id": 1,
        "coun_left": 1,
        "coun_right": 2,
        "lat": 19.43,
        "lon": -99.19,
    }
    defaults.update(kwargs)
    return Colonia.objects.create(**defaults)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class ColoniaModelTest(TestCase):
    def test_str(self):
        c = _make_colonia()
        assert str(c) == "Lomas de Chapultepec (16)"

    def test_default_ordering_by_nombre(self):
        _make_colonia(ckan_id=2, nombre="Tepito")
        _make_colonia(ckan_id=1, nombre="Anzures")
        nombres = list(Colonia.objects.values_list("nombre", flat=True))
        assert nombres == ["Anzures", "Tepito"]

    def test_ckan_id_unique(self):
        from django.db import IntegrityError
        _make_colonia(ckan_id=99)
        with self.assertRaises(IntegrityError):
            _make_colonia(ckan_id=99, nombre="Otra")

    def test_nullable_fields(self):
        c = Colonia.objects.create(ckan_id=10, nombre="Sin coordenadas")
        assert c.lat is None
        assert c.lon is None
        assert c.gid is None


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

class ColoniaAPITest(APITestCase):
    def setUp(self):
        _make_colonia(ckan_id=1, nombre="Tepito", cve_dleg="06")
        _make_colonia(ckan_id=2, nombre="Polanco", cve_dleg="16")
        _make_colonia(ckan_id=3, nombre="Del Valle", cve_dleg="14")

    def test_list_returns_all(self):
        url = reverse("colonia-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3

    def test_retrieve_single(self):
        colonia = Colonia.objects.get(nombre="Tepito")
        url = reverse("colonia-detail", args=[colonia.pk])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nombre"] == "Tepito"
        assert response.data["cve_dleg"] == "06"

    def test_filter_by_cve_dleg(self):
        url = reverse("colonia-list") + "?cve_dleg=16"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["nombre"] == "Polanco"

    def test_search_by_nombre(self):
        url = reverse("colonia-list") + "?search=Valle"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["nombre"] == "Del Valle"

    def test_api_is_read_only(self):
        url = reverse("colonia-list")
        response = self.client.post(url, {"nombre": "Nueva"}, format="json")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_response_fields(self):
        url = reverse("colonia-list")
        response = self.client.get(url)
        record = response.data["results"][0]
        expected = {"id", "ckan_id", "nombre", "clave", "cvegeo", "cve_dleg",
                    "gid", "object_id", "coun_left", "coun_right", "lat", "lon", "updated_at"}
        assert expected == set(record.keys())
