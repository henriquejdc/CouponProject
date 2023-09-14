# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Project imports
from shared.models import BaseModelDate


class Coupon(BaseModelDate):

    COUPON_CHOICES = (
        ('not_general', _('Not general')),
        ('general', _('General')),
    )

    DISCOUNT_CHOICES = (
        ('first_buy', _('First Buy')),
        ('percentage', _('Percentage discount')),
        ('fixed', _('Fixed discount')),
    )

    discount_value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Discount")
    )

    discount_type = models.CharField(
        max_length=100,
        choices=DISCOUNT_CHOICES,
        verbose_name=_("Discount type")
    )

    value_min = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Min. value")
    )

    code = models.CharField(
        unique=True,
        max_length=200,
        verbose_name=_("Code")
    )

    expiration_date = models.DateTimeField(
        verbose_name=_("Expiration date")
    )

    times_used = models.IntegerField(
        verbose_name=_("Times used"),
        default=0
    )

    max_times_used = models.IntegerField(
        verbose_name=_("Times used")
    )

    coupon_type = models.CharField(
        max_length=100,
        choices=COUPON_CHOICES,
        verbose_name=_("Coupon type")
    )

    def __str__(self):
        return f'{self.id} - {self.code} - {self.discount_type} - {self.discount_value}'

    class Meta:
        ordering = ("id",)


class LogCoupon(BaseModelDate):

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.PROTECT,
        verbose_name=_("Coupon")
    )

    total_value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Total value")
    )

    total_discount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Total discount")
    )

    def __str__(self):
        return f'{self.id} - {self.coupon.code} - {self.total_value} - {self.total_discount}'

    class Meta:
        ordering = ("id",)
