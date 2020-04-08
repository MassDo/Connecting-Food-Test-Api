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

class TestProductApi(APITestCase):
    """
    Test the api endpoints '/product/' and '/product/<pk>/'.
    """

    def setUp(self):
        self.client = APIClient()
        # Create instance of Farmer
        self.farmer_1 = Farmer.objects.create(
            nom = 'farmer1',
            numero_siret = 124119812876, # 14 chiffres (9 siren + 5 NIC)
            adresse = 'add1'
        )
        self.farmer_2 = Farmer.objects.create(
            nom = 'farmer2',
            numero_siret = 1234567654, # 14 chiffres (9 siren + 5 NIC)
            adresse = 'add2'
        )

        # Product_1 with farmer 1 & 2
        self.product_1 = Product.objects.create(
            nom = 'product1',
            unite = 4,
            codification_internationnale = 'CI-423',
        )
        self.product_1.producteurs.add(self.farmer_1, self.farmer_2)

        # Product_2 with farmer 2
        self.product_2 = Product.objects.create(
            nom = 'product2',
            unite = 34,
            codification_internationnale = 'CI-4223413213',
        )
        self.product_2.producteurs.add(self.farmer_2)
        
    def test_get_product_list(self):
        """
        test Get /product/ endpoint return all the instances of Product model.
        """
        PRODUCT_URL = reverse('product-list')
        products = Product.objects.all()
        serializer = ProductSerializer(products, context=serializer_context, many=True)
        response = self.client.get(PRODUCT_URL)
        self.assertEqual(response.status_code, 200) # ou status.HTTP_200_OK ?
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data, serializer.data)

    def test_get_product_detail(self):
        """
        test Get /product/1/ return the instace with pk=1 of Product model.
        """
        url = '/product/1/'
        product = Product.objects.get(pk=1)
        serializer = ProductSerializer(product, context=serializer_context)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data, serializer.data)

    def test_create_new_product_with_correct_payload(self):
        """
        test POST: Create a new instance of Product
        """
        url = '/product/'
        payload = {
            'nom' : 'product3',
            'unite' : 23,
            'codification_internationnale' : 'ci',
            'producteurs': [1]
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data['nom'], 'product3')
        self.assertEqual(response.data['producteurs'], [1])
    
    def test_create_new_product_with_incorrect_payload(self):
        """
        test POST: Create a new instance of Product with incorrect data.
        """
        url = '/product/'
        payload = {
            'nom' : 'product3',
            'unite' : 23,
            'codification_internationnale' : 'ci',
            'producteurs': [5] # invalid FK
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertRaises(AssertionError)

    def test_modify_product_with_correct_payload(self):
            """
            test PUT: Modify a instance of Product.
            """
            url = '/product/1/'
            payload = {
                'nom' : 'product1_modified', # modif
                'unite' : 23,
                'codification_internationnale' : 'ci',
                'producteurs': [1,2] # modif
            }
            response = self.client.put(url, payload)
            name = Product.objects.first().nom
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['content-type'], 'application/json')
            self.assertEqual(response.data['nom'], name)

    def test_modify_product_with_incorrect_data(self):
            """
            test PUT: Modify a instance of Product with bad data.
            """
            url = '/product/1/'
            payload = {
                'nom' : 'product1',
                'unite' : 23,
                'codification_internationnale' : 'ci',
                'producteurs': [8] # invalid
            }
            response = self.client.put(url, payload)
            name = Product.objects.first().nom
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response['content-type'], 'application/json')
            self.assertRaises(AssertionError)
    
    def test_delete_product(self):
            """
            test DELETE: delete a instance of Product.
            """
            url = '/product/1/'
            response = self.client.delete(url)
            self.assertEqual(response.status_code, 204)

class TestCertificateApi(APITestCase):
    """
    Test the api endpoints '/certificate/' and '/certificate/<pk>/'.
    """

    def setUp(self):
        self.client = APIClient()
        # Create instance of Farmer
        self.farmer_1 = Farmer.objects.create(
            nom = 'farmer1',
            numero_siret = 124119812876, # 14 chiffres (9 siren + 5 NIC)
            adresse = 'add1'
        )
        self.farmer_2 = Farmer.objects.create(
            nom = 'farmer2',
            numero_siret = 1234567654, # 14 chiffres (9 siren + 5 NIC)
            adresse = 'add2'
        )

        self.certificat_1 = Certificate.objects.create(
            nom = 'certificate1',
            type = 'biologique',
            farmer_certifie = self.farmer_1
        )
        self.certificat_2 = Certificate.objects.create(
            nom = 'certificat2',
            type = 'sans ogm',
            farmer_certifie = self.farmer_2
        )
        
    def test_get_certificate_list(self):
        """
        test Get /certificate/ endpoint return all the instances of Certificate model.
        """
        PRODUCT_URL = reverse('certificate-list')
        certificates = Certificate.objects.all()
        serializer = CertificateSerializer(certificates, context=serializer_context, many=True)
        response = self.client.get(PRODUCT_URL)
        self.assertEqual(response.status_code, 200) # ou status.HTTP_200_OK ?
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data, serializer.data)

    def test_get_certificate_detail(self):
        """
        test Get /certificate/1/ return the instace with pk=1 of Certificate model.
        """
        url = '/certificate/1/'
        certificate = Certificate.objects.get(pk=1)
        serializer = CertificateSerializer(certificate, context=serializer_context)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data, serializer.data)

    def test_create_new_certificate_with_correct_payload(self):
        """
        test POST: Create a new instance of Certificate
        """
        url = '/certificate/'
        payload = {
            'nom': 'certificate3',
            'type': 'biologique',
            'farmer_certifie': 1
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data['nom'], 'certificate3')
        self.assertEqual(response.data['farmer_certifie'], 1)
    
    def test_create_new_certificate_with_incorrect_type_choice(self):
        """
        test POST: Create a new instance of Certificate with incorrect data.
        """
        url = '/certificate/'
        payload = {
            'nom': 'certificate3',
            'type': 'bad-type', # invalid
            'farmer_certifie': 1
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertRaises(AssertionError)

    def test_create_new_certificate_with_incorrect_FK(self):
        """
        test POST: Create a new instance of Certificate with incorrect data.
        """
        url = '/certificate/'
        payload = {
            'nom': 'certificate3',
            'type': 'biologique', # invalid
            'farmer_certifie': [1,2]
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertRaises(AssertionError)
        
    def test_modify_certificate_with_correct_payload(self):
        """
        test PUT: Modify a instance of Certificate.
        """
        url = '/certificate/1/'
        payload = {
            'nom': 'certificate1_modified', # modified
            'type': 'sans ogm', # modified
            'farmer_certifie': 1
        }
        response = self.client.put(url, payload)
        name = Certificate.objects.first().nom
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data['nom'], name)

    def test_modify_product_with_incorrect_data(self):
        """
        test PUT: Modify a instance of Certificate with bad data.
        """
        url = '/certificate/1/'
        payload = {
            'nom': 'certificate1_modified', # modified
            'type': 'bad-type', # modified
            'farmer_certifie': 1
        }
        response = self.client.put(url, payload)
        name = Certificate.objects.first().nom
        self.assertEqual(response.status_code, 400)
        self.assertRaises(AssertionError)
    
    def test_delete_certificate(self):
        """
        test DELETE: delete a instance of Certificate.
        """
        url = '/certificate/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_delete_farmer_delete_certificate_on_cascade(self):
        """
        test DELETE certificate associated to a farmer deletion.
        with our example in setUp: delete farmer_1 must delete on cascade certificate 1. 
        """
        self.client.delete('/farmer/1/')
        response = self.client.get('/certificate/1/')
        self.assertEqual(response.status_code, 404)

    def test_search_certificate_from_farmer_name(self):
        """
        test GET '/certificate/?search=farmer_name' return list of certificate linked to the farmer_name.
        """
        url = '/certificate/'
        payload = {
            'search': 'farmer1'
        }
        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['nom'], 'certificate1')

    def test_search_certificate_from_farmer_name_and_filter_fields_returned(self):
        """
        test GET '/certificate/?search=farmer_name' return list of certificate linked to the farmer_name.
        """
        url = '/certificate/'
        payload = {
            'search': 'farmer1',
            'fields': 'type'
        }
        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['type'], 'biologique')
        with self.assertRaises(KeyError):
            response.data[0]['nom']

class TestSearchProdCertifApi(APITestCase):
    """
    Test the api endpoints '/search-prod-certif/' 
    """
    def setUp(self):
        """
        Resume of the setup of the database:

        farmer 1: certif 1 & product 1
        farmer 2: certif 2 & products (1, 2)
        """
        self.client = APIClient()
        # Create instance of Farmer
        self.farmer_1 = Farmer.objects.create(
            nom = 'farmer1',
            numero_siret = 124119812876, # 14 chiffres (9 siren + 5 NIC)
            adresse = 'add1'
        )
        self.farmer_2 = Farmer.objects.create(
            nom = 'farmer2',
            numero_siret = 1234567654, # 14 chiffres (9 siren + 5 NIC)
            adresse = 'add2'
        )
        # certificate 1 to farmer 1
        self.certificat_1 = Certificate.objects.create(
            nom = 'certificate1',
            type = 'biologique',
            farmer_certifie = self.farmer_1
        )
        # certificate 2 to farmer 2
        self.certificat_2 = Certificate.objects.create(
            nom = 'certificat2',
            type = 'sans ogm',
            farmer_certifie = self.farmer_2
        )
        # Product_1 with farmer 1 & 2
        self.product_1 = Product.objects.create(
            nom = 'product1',
            unite = 4,
            codification_internationnale = 'CI-423',
        )
        self.product_1.producteurs.add(self.farmer_1, self.farmer_2)
        # Product_2 with farmer 2
        self.product_2 = Product.objects.create(
            nom = 'product2',
            unite = 34,
            codification_internationnale = 'CI-4223413213',
        )
        self.product_2.producteurs.add(self.farmer_2)

    def test_search_certificate_and_product_from_farmer_name(self):
        """
        test GET /search-prod-certif/' with filter against the query parameter 'name of the farmer'.
        """
        url = '/search-prod-certif/'
        payload_1 = {
            'search': 'farmer1',
        }
        payload_2 = {
            'search': 'farmer2',
        }
        response = self.client.get(url, payload_1)
        self.assertEqual(response.status_code, 200)

        # assert farmer 1 have certif 1 and product 1
        self.assertEqual(response.data,[
            {'item_type': 'product', 'data': {'id': 1, 'url': 'http://testserver/product/1/', 'nom': 'product1', 'unite': '4', 'codification_internationnale': 'CI-423', 'producteurs': [1, 2]}},
            {'item_type': 'certificate', 'data': {'id': 1, 'url': 'http://testserver/certificate/1/', 'nom': 'certificate1', 'type': 'biologique', 'farmer_certifie': 1}}
        ])
        response = self.client.get(url, payload_2)

        # assert farmer 2 have certif 2 and product 1 & 2
        self.assertEqual(response.data,[
            {'item_type': 'product', 'data': {'id': 1, 'url': 'http://testserver/product/1/', 'nom': 'product1', 'unite': '4', 'codification_internationnale': 'CI-423', 'producteurs': [1, 2]}},
            {'item_type': 'product', 'data': {'id': 2, 'url': 'http://testserver/product/2/', 'nom': 'product2', 'unite': '34', 'codification_internationnale': 'CI-4223413213', 'producteurs': [2]}},
            {'item_type': 'certificate', 'data': {'id': 2, 'url': 'http://testserver/certificate/2/', 'nom': 'certificat2', 'type': 'sans ogm', 'farmer_certifie': 2}}
        ])
