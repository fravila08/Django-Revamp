## students_app/models.py

# models has many different methods we will utilize when creating our Models
from django.db import models
from django.utils import timezone

# models.Model tell Django this is a Model that should be reflected on our database
class Students(models.Model):
    # CharField is a character field and has a default max length of 255 characters
    name = models.CharField(max_length=200, blank=False, null=False)
    # EmailField will automatically check for the existence of a "@" and an ending of ".com/.org/etc."
    email = models.EmailField(unique = True)
    # DateField will accept a date in the following format "YYYY-MM-DD"
    date_of_birth = models.DateField(default="2008-01-01")
    #format "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format."
    last_time_at_school = models.DateTimeField(default=timezone.now())
    # DecimalField will take in decimal numbers 
    daily_allowance = models.DecimalField(max_digits = 5, decimal_places = 2, default=00.00)
    # IntegerField will take in whole numbers 
    year_of_schooling = models.IntegerField(default=10)
    # TextField does not have any maximum character count.
    description = models.TextField(default="Unkown")
    # BooleanField will take in boolean values only
    good_student = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} is in his {self.year_of_schooling} year of schooling and { 'is' if self.good_student else 'is not' } a good student!"
    
    def increase_allowance(self, amount):
        self.daily_allowance += amount
        self.save()
        
    def change_student_status(self):
        self.good_student = not self.good_student
        self.save()