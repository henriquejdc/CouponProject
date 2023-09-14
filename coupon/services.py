# Django imports
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Third party imports
from rest_framework import exceptions

# Project imports
from coupon.models import Coupon, LogCoupon


def use_coupon_service(data: dict) -> dict:
    try:
        coupon = Coupon.objects.get(code=data['coupon_code'])
    except Coupon.DoesNotExist:
        raise exceptions.NotFound({'coupon_code': 'Coupon does not exist'})

    if coupon.expiration_date < timezone.now():
        raise exceptions.ValidationError({'coupon_code': _('Coupon has expired')})

    if coupon.max_times_used <= coupon.times_used:
        raise exceptions.ValidationError({'coupon_code': _('Coupon sold out')})

    if data.get('total_value') < coupon.value_min:
        raise exceptions.ValidationError(
            {'total_value': _('Coupon is not valid for this value. Minimum value is {}').format(
                coupon.value_min
            )}
        )

    response = {
        'coupon_code': coupon.code,
        'total_value': data.get('total_value')
    }

    if coupon.discount_type == 'first_buy' and data.get('first_use') is False:
        raise exceptions.ValidationError({'first_use': _('Coupon valid only for first use')})

    if coupon.discount_type == 'percentage':
        response['discount'] = coupon.discount_value * data.get('total_value') / 100
    else:
        response['discount'] = coupon.discount_value

    response['total_with_discount'] = response['total_value'] - response['discount']

    coupon.times_used += 1
    coupon.save()

    LogCoupon.objects.create(
        coupon=coupon,
        total_value=data.get('total_value'),
        total_discount=response['discount']
    )

    return response
