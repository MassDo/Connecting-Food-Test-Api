from itertools import chain

from rest_framework import filters, generics, views, viewsets
from rest_framework.response import Response

from .models import Certificate, Farmer, Product
from .serializers import (CertificateSerializer, FarmerSerializer,
                          ProductSerializer)


class FarmerView(viewsets.ModelViewSet):
    """
        This view show the Farmer list or instance recorded in database.
    """
    serializer_class = FarmerSerializer
    queryset = Farmer.objects.all()
    
    # si la permission n'est pas ajouté dans le setting du projet
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ProductView(viewsets.ModelViewSet):
    """
        This view show the Product list or instance recorded in database.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
       
class CertificateView(viewsets.ModelViewSet):
    """
        This view show the Certificate list or instance recorded in database.
        If you want you can search by farmer's name with the 'filtrer' button,
        It will return the certificate related to the farmer.
    """
    serializer_class = CertificateSerializer
    queryset = Certificate.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['farmer_certifie__nom']

class ProdAndCertifView(views.APIView):
    """
        This end point aggregate data, it return the products & certificates associated to a farmer name.
        Use the parameter 'search' like this 'GET /search-prod-certif/?search=searched_farmer_name'
    """
    # ovverride the get_queryset method
    def get(self, request):
        # Custom queries
        farmer_name = request.query_params.get('search', None)
        queryset_product = Product.objects.filter(producteurs__nom=farmer_name)
        queryset_certificate = Certificate.objects.filter(
            farmer_certifie__nom=farmer_name
        )
        # Create an iterator for the querysets and turn it into a list.
        results_list = list(chain(queryset_product, queryset_certificate))

        # Build the serialized list of products and certificates from farmer name.
        results = list()
        for entry in results_list:
            item_type = entry.__class__.__name__.lower()
            if isinstance(entry, Product):
                serializer = ProductSerializer(entry, context={'request': request})
            if isinstance(entry, Certificate):
                serializer = CertificateSerializer(entry, context={'request': request})
            
            results.append({'item_type': item_type, 'data': serializer.data})

        return Response(results)
