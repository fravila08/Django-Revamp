from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from .answer_test import *
from .models import *
import json

# Create your tests here.
class Testing_End_Points(TestCase):
    fixtures = ["category.json","product.json"]
    
    def setUp(self):
        self.client = Client()
        
    def test_001_get_products_url_200(self):
        response = self.client.get(reverse('products'))
        self.assertEquals(response.status_code, 200)
        
    def test_002_post_products_url_405(self):
        response = self.client.post(reverse('products'))
        self.assertEquals(response.status_code, 405)
        
    def test_003_put_products_url_405(self):
        response = self.client.put(reverse('products'))
        self.assertEquals(response.status_code, 405)
        
    def test_004_delete_products_url_405(self):
        response = self.client.delete(reverse('products'))
        self.assertEquals(response.status_code, 405)
        
    def test_005_get_products_url_returns_all_products(self):
        response = self.client.get(reverse('products'))
        response_json = json.loads(response.content)
        self.assertEquals(get_products, response_json)
        
    def test_006_get_category_url_200(self):
        response = self.client.get(reverse('category', args=['house']))
        self.assertEquals(response.status_code, 200)
        
    def test_007_post_category_url_405(self):
        response = self.client.post(reverse('category', args=['house']))
        self.assertEquals(response.status_code, 405)
        
    def test_008_put_category_url_405(self):
        response = self.client.put(reverse('category', args=['house']))
        self.assertEquals(response.status_code, 405)
        
    def test_009_delete_category_url_405(self):
        response = self.client.delete(reverse('category', args=['house']))
        self.assertEquals(response.status_code, 405)
        
    def test_010_get_category_url_returns_category_items(self):
        response = self.client.get(reverse('category', args=['house']))
        response_json= json.loads(response.content)
        self.assertEquals(get_category_house, response_json)
        
    def test_011_get_cart_item_url_405(self):
        response = self.client.get(reverse('cart_item', args=[1]))
        self.assertEquals(response.status_code, 405)
        
    def test_012_post_cart_item_url_200(self):
        response = self.client.post(reverse('cart_item', args=[1]))
        with self.subTest():
            self.assertEquals(len(CartItem.objects.all()), 1)
        self.assertEquals(response.status_code, 200)
        
    def test_013_put_cart_item_url_405(self):
        response = self.client.put(reverse('cart_item', args=[1]))
        self.assertEquals(response.status_code, 405)
        
    def test_014_delete_cart_item_url_200(self):
        self.client.post(reverse('cart_item', args=[1]))
        with self.subTest():
            self.assertEquals(len(CartItem.objects.all()), 1)
        response = self.client.delete(reverse('cart_item', args=[1]))
        with self.subTest():
            self.assertEquals(len(CartItem.objects.all()), 0)
        self.assertEquals(response.status_code, 200)
        
    def test_015_get_cart_item_edit_url_405(self):
        self.client.post(reverse('cart_item', args=[1]))
        response = self.client.get(reverse('cart_item_edit', args=[1, 'add']))
        self.assertEquals(response.status_code, 405)
        
    def test_016_post_cart_item_edit_url_405(self):
        self.client.post(reverse('cart_item', args=[1]))
        response = self.client.post(reverse('cart_item_edit', args=[1, 'add']))
        self.assertEquals(response.status_code, 405)
        
    def test_017_put_cart_item_edit_add_url_200(self):
        self.client.post(reverse('cart_item', args=[1]))
        response = self.client.put(reverse('cart_item_edit', args=[1, 'add']))
        with self.subTest():
            self.assertEquals(CartItem.objects.get(product= Product.objects.get(id = 1)).quantity, 2)
        self.assertEquals(response.status_code, 200)
        
    def test_018_put_cart_item_edit__drop_url_200(self):
        self.client.post(reverse('cart_item', args=[1]))
        self.client.put(reverse('cart_item_edit', args=[1, 'add']))
        response = self.client.put(reverse('cart_item_edit', args=[1, 'drop']))
        with self.subTest():
            self.assertEquals(CartItem.objects.get(product= Product.objects.get(id = 1)).quantity, 1)
        self.assertEquals(response.status_code, 200)
        
    def test_019_delete_cart_item_edit_url_405(self):
        self.client.post(reverse('cart_item', args=[1]))
        response = self.client.delete(reverse('cart_item_edit', args=[1, 'add']))
        self.assertEquals(response.status_code, 405)
        
    def test_020_get_cart_url_200(self):
        response = self.client.get(reverse('cart'))
        self.assertEquals(response.status_code, 200)
        
    def test_021_post_cart_url_405(self):
        response = self.client.post(reverse('cart'))
        self.assertEquals(response.status_code, 405)
        
    def test_022_put_cart_url_405(self):
        response = self.client.put(reverse('cart'))
        self.assertEquals(response.status_code, 405)
        
    def test_023_delete_cart_url_405(self):
        response = self.client.delete(reverse('cart'))
        self.assertEquals(response.status_code, 405)
        
    def test_024_get_cart_url_returns_cart_items(self):
        for i in range(1,6):
            self.client.post(reverse('cart_item', args=[i]))
        response = self.client.get(reverse('cart'))
        response_json = json.loads(response.content)
        self.assertEquals(response_json, get_cart_items)
        
    def test_025_get_product_by_name_url_200(self):
        response = self.client.get(reverse('product', args=['Visor']))
        self.assertEquals(response.status_code, 200)
    
    def test_026_put_product_by_name_url_405(self):
        response = self.client.put(reverse('product', args=['Visor']))
        self.assertEquals(response.status_code, 405)
        
    def test_027_post_product_by_name_url_405(self):
        response = self.client.post(reverse('product', args=['Visor']))
        self.assertEquals(response.status_code, 405)
        
    def test_028_delete_product_by_name_url_405(self):
        response = self.client.delete(reverse('product', args=['Visor']))
        self.assertEquals(response.status_code, 405)
        
    def test_029_get_product_by_name_url_returns_visor(self):
        response = self.client.get(reverse('product', args=['Visor']))
        response_json = json.loads(response.content)
        self.assertEquals(response_json, get_product_by_name)
        
    """THE FOLLOWING WILL BE CONSIDERED EXTRA CREDIT"""
    def test__product_price_validator(self):
        product = Product.objects.create(name="Testing", price = 10.3798, description="this should fail", category = Category.objects.get(id =1))
        try:
            product.full_clean()
            self.fail()
        except ValidationError as e:
            self.assertEquals(['Ensure that there are no more than 2 decimal places.', 'Ensure that there are no more than 2 decimal places.'], e.message_dict['price'])
            
    def test__category_acceptable_validator(self):
        category = Category.objects.create(title = 'ecrdytfvgyb')
        try:
            category.full_clean()
            self.fail()
        except ValidationError as e:
            self.assertTrue('This category does not exist!' in e.message_dict['title'])
            
    def test__cart_item_invalid_quantity(self):
        item = CartItem(product = Product.objects.get(id =1), quantity = -5)
        try:
            item.full_clean()
            self.fail()
        except ValidationError as e:
            self.assertTrue('Ensure this value is greater than or equal to 1.' in e.message_dict['quantity'])
            