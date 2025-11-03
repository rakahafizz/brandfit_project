from django.test import TestCase
from ..models import Product

class ProductModelTest(TestCase):
    def test_slug_is_generated(self):
        p = Product.objects.create(name='Test Product Slug')
        self.assertTrue(p.slug.startswith('test-product-slug'))
