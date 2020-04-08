from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from api.models import Certificate, Farmer, Product
from api.serializers import (CertificateSerializer, FarmerSerializer,
                             ProductSerializer)

# context, solution trouvée sur SO
factory = APIRequestFactory()
request = factory.get('/')

serializer_context = {
    'request': Request(request),
}


class TestFarmerApi(APITestCase):
    """
    Test the api endpoints '/farmer/' and '/farmer/<pk>/'.
    """

    def setUp(self):
        self.client = APIClient()
        # Create instance of Farmer
        Farmer.objects.create(
            nom = 'farmer1',
            numero_siret = 124119812876, # 14 chiffres (9 siren + 5 NIC)
            adresse = 'add1'
        )
        Farmer.objects.create(
            nom = 'farmer2',
            numero_siret = 1234567654, # 14 chiffres (9 siren + 5 NIC)
            adresse = 'add2'
        )
        
    def test_get_farmer_list(self):
        """
        test Get /farmer/ endpoint return alle the instances of Farmer model.
        """
        FARMER_URL = reverse('farmer-list')
        farmers = Farmer.objects.all()
        serializer = FarmerSerializer(farmers, context=serializer_context, many=True)
        response = self.client.get(FARMER_URL)
        self.assertEqual(response.status_code, 200) # ou status.HTTP_200_OK ?
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data, serializer.data)

    def test_get_farmer_detail(self):
        """
        test Get /farmer/1/ return the instace with pk=1 of Farmer model.
        """
        url = '/farmer/1/'
        farmer = Farmer.objects.get(pk=1)
        serializer = FarmerSerializer(farmer, context=serializer_context)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data, serializer.data)

    def test_create_new_farmer_with_correct_payload(self):
        """
        test POST: Create a new instance of Farmer
        """
        url = '/farmer/'
        payload = {
            'nom' : 'farmer3',
            'numero_siret' : 12324134,
            'adresse' : 'add3'
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data['nom'], 'farmer3')
    
    def test_create_new_farmer_with_incorrect_payload(self):
        """
        test POST: Create a new instance of Farmer with incorrect data.
        """
        url = '/farmer/'
        payload = {
            'nom' : False, # CharField
            'numero_siret' : 12324134,
            'adresse' : 'add3'
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertRaises(AssertionError)

    def test_modify_farmer_with_correct_payload(self):
            """
            test PUT: Modify a instance of Farmer.
            """
            url = '/farmer/1/'
            payload = {
                'id': 1,
                'nom' : 'farmer1_modify',
                'numero_siret' : 12324134,
                'adresse' : 'add3'
            }
            response = self.client.put(url, payload)
            name = Farmer.objects.first().nom
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['content-type'], 'application/json')
            self.assertEqual(response.data['nom'], name)

    def test_modify_farmer_with_incorrect_data(self):
            """
            test PUT: Modify a instance of Farmer.
            """
            url = '/farmer/1/'
            payload = {
                'id': 1,
                'nom' : False,
                'numero_siret' : 12324134,
                'adresse' : 'add3'
            }
            response = self.client.put(url, payload)
            name = Farmer.objects.first().nom
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response['content-type'], 'application/json')
            self.assertRaises(AssertionError)
    
    def test_delete_farmer(self):
            """
            test DELETE: delete a instance of Farmer.
            """
            url = '/farmer/1/'
            response = self.client.delete(url)
            self.assertEqual(response.status_code, 204)