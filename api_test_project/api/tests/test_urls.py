from django.urls import resolve
from rest_framework.test import APITestCase

class TestUrls(APITestCase):

    def test_views_names(self):
        """
            Check if the name of url is linked to the
            correct path.
        """
        # url = reverse('farmer-list')
        # Test name linked to url
        self.assertEqual(resolve('/farmer/').view_name, 'farmer-list')
        self.assertEqual(resolve('/farmer/2/').view_name, 'farmer-detail')
        self.assertEqual(resolve('/product/').view_name, 'product-list')
        self.assertEqual(resolve('/product/2/').view_name, 'product-detail')
        self.assertEqual(resolve('/certificate/').view_name, 'certificate-list')
        self.assertEqual(resolve('/certificate/2/').view_name, 'certificate-detail')
        self.assertEqual(resolve('/search-prod-certif/').view_name, 'search-prod-certif-list')