from rest_framework.routers import SimpleRouter

from coupon.views import CouponViewSet


router = SimpleRouter()
router.register(r'', CouponViewSet, basename='coupon')
urlpatterns = router.urls
