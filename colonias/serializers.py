from rest_framework import serializers
from .models import Colonia


class ColoniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colonia
        fields = [
            "id",
            "ckan_id",
            "nombre",
            "clave",
            "cvegeo",
            "cve_dleg",
            "gid",
            "object_id",
            "coun_left",
            "coun_right",
            "lat",
            "lon",
            "updated_at",
        ]
