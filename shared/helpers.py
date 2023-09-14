# Base imports
try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict
from functools import partial
import math
from rest_framework.pagination import PageNumberPagination


sign = partial(math.copysign, 1)


class DefaultPaginationClass(PageNumberPagination):
    page_size_query_param = "page_size"

