from rest_framework import status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.utils.filters_utils import perform_product_list_filters
from api.utils.renderers import ProductListResponseRenderer
from apps.shop.models import Product
from api.serializers.shop import ProductSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


# class ProductListCreateView(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = ['stock']
#     search_fields = ['name']


@extend_schema(
    summary="Create product",
    description="Creates a new product",
    methods=["POST"],
    operation_id="productCreate",
    tags=["Shop"],
    responses=OpenApiResponse(ProductSerializer),
)
class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema_view(
    get=extend_schema(
        summary="All Product List with filter and search",
        description="List of all products with filter and search",
        methods=["get"],
        operation_id="productList",
        tags=["Shop"],
        parameters=[
            OpenApiParameter(
                "from_date_iso",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                many=False,
                description="Date Range Filter: beginning date (yy-mm-dd)",
            ),
            OpenApiParameter(
                "to_date_iso",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                many=False,
                description="Date Range Filter: end date (yy-mm-dd)",
            ),
            OpenApiParameter(
                "status",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                many=False,
                description="Filter by product by status: Draft or Published",
            ),
        ],
        responses=ProductSerializer,
    )
)
class ProductListView(ListAPIView):
    queryset: tuple = Product.objects.none()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name"]
    permission_classes: list = []
    renderer_classes = [ProductListResponseRenderer]
    # pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        perform_filter = perform_product_list_filters(self.request)
        queryset = perform_filter.filter_queryset(queryset)
        return queryset


@extend_schema_view(
    get=extend_schema(
        summary="Get single product",
        description="Get single product",
        methods=["get"],
        operation_id="productRetrieve",
        tags=["Shop"],
        responses=ProductSerializer,
    ),
    put=extend_schema(
        summary="Updates single product",
        description="Updates single product",
        methods=["put"],
        operation_id="productUpdate",
        tags=["Shop"],
        responses=OpenApiResponse(ProductSerializer),
    ),
    delete=extend_schema(
        summary="Removes single product",
        description="Removes single product",
        methods=["delete"],
        operation_id="productDlete",
        tags=["Shop"],
        responses=None,
    )
)
class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    
