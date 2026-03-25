import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import SiniestroVial
from .tasks import _calcular_estadisticas_siniestros


def _siniestro(ckan_id=1, alcaldia="Cuauhtémoc", tipo_evento="Colisión",
               fecha=None, colonia="Centro", lesionados=1, fallecidos=0, **kw):
    return SiniestroVial.objects.create(
        ckan_id=ckan_id,
        alcaldia=alcaldia,
        tipo_evento=tipo_evento,
        fecha=fecha or datetime.date(2024, 3, 1),
        colonia=colonia,
        lesionados=lesionados,
        fallecidos=fallecidos,
        latitud=19.43,
        longitud=-99.13,
        vehiculos_involucrados=2,
        **kw,
    )


# ── Model tests ───────────────────────────────────────────────────────────────

class SiniestroVialModelTest(TestCase):
    def test_str(self):
        s = _siniestro()
        assert "Colisión" in str(s)
        assert "Cuauhtémoc" in str(s)

    def test_ckan_id_unique(self):
        from django.db import IntegrityError
        _siniestro(ckan_id=1)
        with self.assertRaises(IntegrityError):
            _siniestro(ckan_id=1)

    def test_nullable_coords(self):
        s = SiniestroVial.objects.create(
            ckan_id=99, alcaldia="Tlalpan", tipo_evento="Atropellamiento",
        )
        assert s.latitud is None
        assert s.longitud is None


# ── API tests ─────────────────────────────────────────────────────────────────

class SiniestroVialAPITest(APITestCase):
    def setUp(self):
        _siniestro(ckan_id=1, alcaldia="Cuauhtémoc", tipo_evento="Colisión",
                   colonia="Centro", lesionados=2)
        _siniestro(ckan_id=2, alcaldia="Iztapalapa", tipo_evento="Atropellamiento",
                   colonia="Ermita", lesionados=1, fallecidos=1)
        _siniestro(ckan_id=3, alcaldia="Cuauhtémoc", tipo_evento="Atropellamiento",
                   colonia="Tepito", lesionados=0)

    def test_list_all(self):
        url = reverse("siniestrovial-list")
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 3

    def test_filter_by_alcaldia(self):
        url = reverse("siniestrovial-list") + "?alcaldia=Cuauhtémoc"
        resp = self.client.get(url)
        assert resp.data["count"] == 2

    def test_filter_by_tipo_evento(self):
        url = reverse("siniestrovial-list") + "?tipo_evento=Atropellamiento"
        resp = self.client.get(url)
        assert resp.data["count"] == 2

    def test_filter_combined(self):
        url = reverse("siniestrovial-list") + "?alcaldia=Cuauhtémoc&tipo_evento=Colisión"
        resp = self.client.get(url)
        assert resp.data["count"] == 1

    def test_search_by_colonia(self):
        url = reverse("siniestrovial-list") + "?search=Tepito"
        resp = self.client.get(url)
        assert resp.data["count"] == 1

    def test_retrieve(self):
        s = SiniestroVial.objects.first()
        url = reverse("siniestrovial-detail", args=[s.pk])
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK

    def test_read_only(self):
        url = reverse("siniestrovial-list")
        resp = self.client.post(url, {})
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


# ── Celery task tests ─────────────────────────────────────────────────────────

class EstadisticasSiniestrosTest(TestCase):
    def setUp(self):
        _siniestro(ckan_id=1, alcaldia="Cuauhtémoc", tipo_evento="Colisión",
                   lesionados=2, fallecidos=0)
        _siniestro(ckan_id=2, alcaldia="Cuauhtémoc", tipo_evento="Colisión",
                   lesionados=1, fallecidos=1)
        _siniestro(ckan_id=3, alcaldia="Iztapalapa", tipo_evento="Atropellamiento",
                   lesionados=0, fallecidos=1)

    def test_returns_list(self):
        result = _calcular_estadisticas_siniestros()
        assert isinstance(result, list)

    def test_groups_by_alcaldia_tipo(self):
        result = _calcular_estadisticas_siniestros()
        keys = {(r["alcaldia"], r["tipo_evento"]) for r in result}
        assert ("Cuauhtémoc", "Colisión") in keys
        assert ("Iztapalapa", "Atropellamiento") in keys

    def test_count_aggregation(self):
        result = _calcular_estadisticas_siniestros()
        cuauh = next(r for r in result
                     if r["alcaldia"] == "Cuauhtémoc" and r["tipo_evento"] == "Colisión")
        assert cuauh["total"] == 2
        assert cuauh["total_lesionados"] == 3
        assert cuauh["total_fallecidos"] == 1
