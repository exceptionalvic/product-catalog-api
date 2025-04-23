import logging
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

logger = logging.getLogger(__name__)


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

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Product creation failed: {str(e)}")
            return Response(
                {"detail": "Unable to create product."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
    
    def get_queryset(self):
        try:
            queryset = Product.objects.all()
            perform_filter = perform_product_list_filters(self.request)
            return perform_filter.filter_queryset(queryset)
        except Exception as e:
            logger.error(f"Error while filtering product list: {str(e)}")
            return Product.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Product list fetch failed: {str(e)}")
            return Response(
                {"detail": f"Unable to fetch product list. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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


    def retrieve(self, request, *args, **kwargs):
        try:
            check_prod = Product.objects.filter(id=kwargs['id']).exists()
            if not check_prod:
                return Response(
                    {"detail": "Product not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Retrieve product failed: {str(e)}")
            return Response(
                {"detail": "Unable to retrieve product."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            check_prod = Product.objects.filter(id=kwargs['id']).exists()
            if not check_prod:
                return Response(
                    {"detail": "Product not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Update product failed: {str(e)}")
            return Response(
                {"detail":f"Unable to update product. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        try:
            check_prod = Product.objects.filter(id=kwargs['id']).exists()
            if not check_prod:
                return Response(
                    {"detail": "Product not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Delete product failed: {str(e)}")
            return Response(
                {"detail": f"Unable to delete product. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
