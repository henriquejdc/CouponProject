from django.contrib import admin

from .models import Coupon, LogCoupon


admin.site.register(Coupon)
admin.site.register(LogCoupon)
