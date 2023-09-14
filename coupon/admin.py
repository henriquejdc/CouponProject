# Django imports
from django.contrib import admin

# Project imports
from .models import Coupon, LogCoupon


admin.site.register(Coupon)
admin.site.register(LogCoupon)
