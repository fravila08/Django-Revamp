from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import School

# Create your tests here.
class school_test(TestCase):
    
    def test_01_create_school_instance(self):
        new_school = School(name = 'Code Platoon')
        try:
            new_school.full_clean()
            self.assertIsNotNone(new_school)
        except ValidationError as e:
            # print(e.message_dict)
            self.fail()
        
    def test_02_create_school_with_incorrect_name_length(self):
        new_school = School(name='Nope')
        try:
            new_school.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assertTrue('Ensure this value has at least 5 characters (it has 4).' in e.message_dict['name'])