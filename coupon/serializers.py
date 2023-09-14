# Base imports
from typing import OrderedDict

# Django imports
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Third-party imports
from rest_framework import serializers

# Project imports
from coupon.models import Coupon


class CreateCouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = (
            'discount_value',
            'discount_type',
            'value_min',
            'code',
            'expiration_date',
            'max_times_used',
            'coupon_type',
        )

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if timezone.now() > attrs.get('expiration_date'):
            raise serializers.ValidationError(
                {
                    'expiration_date': _("Expiration date must be greater than the creation date")
                }
            )

        if attrs.get('discount_type') == 'percentage':
            if attrs.get('discount_value') > 100 or attrs.get('discount_value') < 0:
                raise serializers.ValidationError(
                    {
                        'discount_value': _("Discount percentage range is from 0 to 100")
                    }
                )
        else:
            if attrs.get('discount_value') > attrs.get('value_min'):
                raise serializers.ValidationError(
                    {
                        'value_min': _("Minimum value must be less than discount")
                    }
                )
        return super().validate(attrs)


class GetCouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = '__all__'


class UseCouponSerializer(serializers.Serializer):

    total_value = serializers.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    first_use = serializers.BooleanField()

    coupon_code = serializers.CharField(
        max_length=200
    )
