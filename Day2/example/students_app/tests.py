from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Students, Exchange_Student# import Student, and Exchange model
from school_app.models import School

# Create your tests here.
class student_test(TestCase):
    
    def setUp(self):
        # Create a new School
        new_school = School(name = 'Code Platoon')
        new_school.save()
        second_school = School(name= 'Code Academy')
        second_school.save()
    
    def test_01_create_student_instance(self):
        # Here we will create our Student instance
        new_studet = Students(name="Nick Cage", email="nick@gmail.com", year_of_schooling=2, description="Nick Cage is an excellent student that gives his classes everything he can all the time every time.")
        try:
            # remember validators are not ran on our new instance until we run full_clean
            new_studet.full_clean()
            # here we will ensure our instance is actually created
            self.assertIsNotNone(new_studet)
        except ValidationError as e:
            # print(e.message_dict)
            #if it sends an error we want to ensure this test fails
            self.fail()
        
    def test_02_create_student_with_incorrect_name_format(self):
        # we create an instance with an improper name
        new_studet = Students(name='pancho 23 V1lla', email='pancho@gmail.com', description="Panch was an ok student that his best but really struggled.")
        try:
            new_studet.full_clean()
            # if our instance runs through the full clean and doesn't throw an error, than we
            # know our validator is not working correctly and we should fail this test 
            self.fail()

        except ValidationError as e:
            # print(e.message_dict)
            # we can ensure the correct message is inside our ValidationError
            self.assertTrue('Improper name format please enter First and Last seperated by a space and with proper capitalization' in e.message_dict['name'])

    def test_03_create_exchange_student(self):
        # Here we can create an exchange student
        exchange_stud = Exchange_Student(name="Nick Cage", email="nick@gmail.com", year_of_schooling=2, description="Nick Cage is an excellent student that gives his classes everything he can all the time every time.", school = School.objects.all().first())
        # Now we need to save our student in order to be able to access it's manyTomany relationships
        exchange_stud.save()
        # Many to many relationships are treated as sets in python so now we utilize the add function to place ids into this field
        exchange_stud.other_schools.add(6)
        try:
            exchange_stud.full_clean()
            self.assertIsNotNone(exchange_stud)
        except ValidationError as e:
            print(e.message_dict)
            self.fail()