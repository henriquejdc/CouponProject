# Django imports
from django.utils.translation import gettext_lazy as _
from django.http.response import HttpResponse

# Third party imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

# Project imports
from coupon.models import Coupon
from coupon.serializers import (
    GetCouponSerializer,
    CreateCouponSerializer, UseCouponSerializer
)
from coupon.services import use_coupon_service
from shared.http.responses import api_exception_response
from shared.views import BaseCollectionViewSet


class CouponViewSet(BaseCollectionViewSet):
    """ A ViewSet for retrieving Coupon. """
    model_class = Coupon
    queryset = model_class.objects.all()
    serializer_class = GetCouponSerializer
    http_method_names = ('get', 'post')
    serializers = {
        'default': serializer_class,
        'create': CreateCouponSerializer,
        'use_coupon': UseCouponSerializer,
    }
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], name=_("Use Coupon"))
    def use_coupon(self, request: Request) -> HttpResponse:
        try:
            serializer = UseCouponSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                response_data = use_coupon_service(serializer.validated_data)
                return Response(status=status.HTTP_200_OK, data=response_data)
        except Exception as exception:
            return api_exception_response(exception=exception)
