## students_app/models.py

# models has many different methods we will utilize when creating our Models
from django.db import models
from django.utils import timezone
# import built-in Django Validators
from django.core import validators as v
# importing custom Validators
from .validators import validate_name
# import School model
from school_app.models import School


class Students(models.Model):
    # This will likely need a custom validator
    name = models.CharField(max_length=200, blank=False, null=False, validators=[validate_name])
    # Validate Email is already running under the hood of EmailField but 
    # if I were to mannually add it to a field it would like like this
    email = models.EmailField(unique = True, validators=[v.validate_email])
    # Under the hood DateField is already running a regex funciton to ensure input 
    # is matching the correct date format of "YYYY-MM-DD"
    date_of_birth = models.DateField(default="2008-01-01")
    # Under the hood DateField is already running a regex funciton to ensure input 
    # is matching the correct date format of "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"
    last_time_at_school = models.DateTimeField(default=timezone.now())
    # DecimalField has it's own validator and takes the same arguments as the field itself.
    daily_allowance = models.DecimalField(max_digits=5, decimal_places=2, default=00.00, validators=[v.DecimalValidator(5, 2)])
    # Lets change this into a PositiveIntegerField since that's what we want an add an 
    # calidation to ensure only int types could be passed onto this field. Lets also add a max and 
    # min value to years of schooling.
    year_of_schooling = models.PositiveIntegerField(default=10, validators=[v.integer_validator, v.MinValueValidator(1), v.MaxValueValidator(27)])
    # We don't want a student's description to either be too long or too short so
    # lets add both a Max and Min LengthValidators to our TextField to ensure
    # input meets our criteria
    description = models.TextField(validators=[v.MaxLengthValidator(500), v.MinLengthValidator(50)])
    # Boolean field is already ensuring to only take in either True or False
    good_student = models.BooleanField(default=True)
    # Creating a MANY Students to ONE School relationship and setting Code Platoon as the default value
    school = models.ForeignKey(School, on_delete = models.CASCADE, default = 1)
    

    
    def __str__(self):
        return f"{self.name} is in his {self.year_of_schooling} year of schooling and { 'is' if self.good_student else 'is not' } a good student!"
    
    def increase_allowance(self, amount):
        self.daily_allowance += amount
        self.save()
        
    def change_student_status(self):
        self.good_student = not self.good_student
        self.save()
        
# Lets utilize inheritance to utilize all of our Students Models fields
class Exchange_Student(Students):
    # Now we could simply add a field to our Exchange_Student model
    other_schools = models.ManyToManyField(School, related_name = 'exchange_students')
    # the related fields argument creates the ability for the School model to grab this field 
    # through exchange_students