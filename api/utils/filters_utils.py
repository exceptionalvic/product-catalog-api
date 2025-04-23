from django.db.models import Q, OuterRef, Subquery, F
from django.db.models.functions import Coalesce
from apps.shop.models import Product
from datetime import timedelta, datetime
from rest_framework.serializers import ValidationError
from django.db.models import F, Value, CharField
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class perform_product_list_filters:

    def __init__(self, request):
        self.request = request

    def filter_by_period(self, queryset, from_date_iso, to_date_iso):
        """ Filters products by date range of creation"""
        # Convert ISO format to datetime objects
        from_date = datetime.fromisoformat(from_date_iso)
        to_date = datetime.fromisoformat(to_date_iso)

        if from_date is not None and to_date is not None:
            try:
                queryset = queryset.filter(Q(created_at__date__gte=from_date),Q(created_at__date__lte=to_date))
            except Exception as e:
                raise ValidationError({'detail': f'{str(e)}'})
        else:
            raise ValueError({'detail': f'date filter must have from_date and to_date ranges to work'})

        return queryset

    def filter_queryset(self, queryset):
        from_date_period = self.request.GET.get("from_date_iso", None)
        to_date_period = self.request.GET.get("to_date_iso", None)
        product_status = self.request.GET.get("status", None)

        # queryset = self.get_queryset()
        try:
            if from_date_period and to_date_period:
                queryset = self.filter_by_period(queryset, from_date_period, to_date_period)
                            

            if product_status:
                if product_status == "Draft":
                    queryset = queryset.filter(is_published=False)
                elif product_status == "Published":
                    queryset = queryset.filter(is_published=True)

        except Exception as e:
            print("Error:", e)
            logger.error(f"Error@filter_queryset: {e}")
        return queryset