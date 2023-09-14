import json
from typing import List

from django.urls import reverse
from django.utils import timezone
from model_bakery import baker
from rest_framework import status

from coupon.serializers import GetCouponSerializer
from shared.tests import BaseAPITestCase


class CouponViewSetViewSetTestCase(BaseAPITestCase):
    """Test all scenarios for CouponViewSet."""

    tests_to_perform: List = [
        'create_ok',
        'create_validation_error',
        'list',
        'retrieve',
    ]

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("coupon-list")
        self.test_protected_error = False
        self.validation_error_column = 'code'
        self.ignored_keys_from_response += ['expiration_date']
        self.row_object = baker.make(
            "coupon.Coupon",
            code="TESTEROWOBJECT",
        )
        self.coupon_percentage = baker.make(
            "coupon.Coupon",
            discount_value=10,
            value_min=30,
            discount_type="percentage",
            code="PERCENTAGE",
            expiration_date=(timezone.now() + timezone.timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            max_times_used=10,
            coupon_type="general"
        )
        self.coupon_fixed = baker.make(
            "coupon.Coupon",
            discount_value=10,
            value_min=30,
            discount_type="fixed",
            code="FIXED",
            expiration_date=(timezone.now() + timezone.timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            max_times_used=10,
            coupon_type="general"
        )
        self.coupon_expired = baker.make(
            "coupon.Coupon",
            discount_value=10,
            value_min=30,
            discount_type="fixed",
            code="EXPIRED",
            expiration_date=(timezone.now() - timezone.timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            max_times_used=10,
            coupon_type="general"
        )
        self.coupon_total_used = baker.make(
            "coupon.Coupon",
            discount_value=10,
            value_min=30,
            discount_type="fixed",
            code="TOTALUSED",
            expiration_date=(timezone.now() + timezone.timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            times_used=10,
            max_times_used=10,
            coupon_type="general"
        )
        self.row_object_no_relation = self.row_object

        self.post_data = {
            "discount_value": "10.00",
            "discount_type": "first_buy",
            "value_min": "30.00",
            "code": "FIRSTUSE",
            "expiration_date": (timezone.now() + timezone.timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            "max_times_used": 20,
            "coupon_type": "general"
        }
        self.total_rows = 5
        self.http_404_error_description = "No Coupon matches the given query."

    def set_test_retrieve_fields(self):
        data = GetCouponSerializer(self.row_object).data
        self.retrieve_test_fields = data

    # TESTS FOR OK USED COUPON

    def test_ok_fixed_coupon_discount(self):
        response = self.client.post(
            f'{self.url}use_coupon/',
            data={
              "total_value": "30.00",
              "first_use": True,
              "coupon_code": self.coupon_fixed.code
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents,
            {
                'coupon_code': self.coupon_fixed.code,
                'total_value': 30.0,
                'discount': 10.0,
                'total_with_discount': 20.0
            }
        )

    def test_ok_percentage_coupon_discount(self):
        response = self.client.post(
            f'{self.url}use_coupon/',
            data={
              "total_value": "30.00",
              "first_use": True,
              "coupon_code": self.coupon_percentage.code
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents,
            {
                'coupon_code': self.coupon_percentage.code,
                'total_value': 30.0,
                'discount': 3.0,
                'total_with_discount': 27.0
            }
        )

    def test_ok_first_use_coupon_discount(self):
        response = self.client.post(
            self.url,
            data=self.post_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.post(
            f'{self.url}use_coupon/',
            data={
              "total_value": "30.00",
              "first_use": True,
              "coupon_code": "FIRSTUSE"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents,
            {
                'coupon_code': "FIRSTUSE",
                'total_value': 30.0,
                'discount': 10.0,
                'total_with_discount': 20.0
            }
        )

    # TESTS FOR ERRORS USED COUPON

    def test_duplicate_coupon(self):
        response = self.client.post(
            self.url,
            data=self.post_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            self.url,
            data=self.post_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents['description'],
            {"detail": {"code": ["coupon with this Code already exists."]}}
        )

    def test_bad_request_expired(self):
        data = self.post_data
        data['expiration_date'] = (timezone.now() - timezone.timedelta(days=1)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        response = self.client.post(
            self.url,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents['description'],
            {"detail": {"expiration_date": ["Expiration date must be greater than the creation date"]}}
        )

    def test_bad_request_discount_value(self):
        data = self.post_data
        data['discount_value'] = "50"

        response = self.client.post(
            self.url,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents['description'],
            {"detail": {"value_min": ["Minimum value must be less than discount"]}}
        )

    def test_bad_request_discount_percent_value(self):
        data = self.post_data
        data['discount_value'] = "500"
        data['discount_type'] = "percentage"

        response = self.client.post(
            self.url,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents['description'],
            {"detail": {"discount_value": ["Discount percentage range is from 0 to 100"]}}
        )

    def test_not_found_code_coupon(self):
        response = self.client.post(
            f'{self.url}use_coupon/',
            data={
              "total_value": "30.00",
              "first_use": True,
              "coupon_code": "FIRSTUSE1111111111111111111111111111"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents['description'],
            {"detail": {'coupon_code': 'Coupon does not exist'}}
        )

    def test_expired_coupon(self):
        response = self.client.post(
            f'{self.url}use_coupon/',
            data={
              "total_value": "30.00",
              "first_use": True,
              "coupon_code": self.coupon_expired.code
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents['description'],
            {"detail": {'coupon_code': 'Coupon has expired'}}
        )

    def test_sold_out_coupon(self):
        response = self.client.post(
            f'{self.url}use_coupon/',
            data={
              "total_value": "30.00",
              "first_use": True,
              "coupon_code": self.coupon_total_used.code
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents['description'],
            {"detail": {'coupon_code': 'Coupon sold out'}}
        )

    def test_min_value_coupon(self):
        response = self.client.post(
            f'{self.url}use_coupon/',
            data={
              "total_value": "3.00",
              "first_use": True,
              "coupon_code": self.coupon_fixed.code
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents['description'],
            {"detail": {'total_value': 'Coupon is not valid for this value. Minimum value is 30.00'}}
        )

    def test_not_first_use_coupon(self):
        response = self.client.post(
            self.url,
            data=self.post_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            f'{self.url}use_coupon/',
            data={
              "total_value": "30.00",
              "first_use": False,
              "coupon_code": "FIRSTUSE"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contents = json.loads(response.content)
        self.assertDictEqual(
            contents['description'],
            {"detail": {'first_use': 'Coupon valid only for first use'}}
        )
