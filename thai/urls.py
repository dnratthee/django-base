from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from thai.models import District, SubDistrict


@permission_classes([IsAuthenticated])
class ZipcodeSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField(read_only=True)
    province = serializers.StringRelatedField(
        source="district.province", read_only=True
    )
    district_id = serializers.PrimaryKeyRelatedField(read_only=True)
    province_id = serializers.PrimaryKeyRelatedField(
        source="district.province", read_only=True
    )

    class Meta:
        model = SubDistrict
        fields = [
            "id",
            "zipcode",
            "name",
            "district",
            "province",
            "district_id",
            "province_id",
        ]


@permission_classes([IsAuthenticated])
class ZipcodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubDistrict.objects.all()
    serializer_class = ZipcodeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["zipcode"]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, format=None):
        if request.GET.get("zipcode"):
            return super().list(request, format)
        else:
            return Response([])  # return empty list if no zipcode is provided


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["id", "name"]


@permission_classes([IsAuthenticated])
class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["province"]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, format=None):
        if request.GET.get("province"):
            return super().list(request, format)
        else:
            return Response([])  # return empty list if no province is provided


class SubDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDistrict
        fields = ["id", "name", "zipcode"]


@permission_classes([IsAuthenticated])
class SubDistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubDistrict.objects.all()
    serializer_class = SubDistrictSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["district"]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, format=None):
        if request.GET.get("district"):
            return super().list(request, format)
        else:
            return Response([])  # return empty list if no district is provided


urlpatterns = [
    path(
        "api/address/", ZipcodeViewSet.as_view({"get": "list"})
    ),  # /api/address/?zipcode=12345
    path(
        "api/districts/", DistrictViewSet.as_view({"get": "list"})
    ),  # /api/districts/?province=1
    path(
        "api/sub_districts/", SubDistrictViewSet.as_view({"get": "list"})
    ),  # /api/sub_districts/?district=1
]
