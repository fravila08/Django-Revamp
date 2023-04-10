# This will allow us to throw a validation error when interacting with 
# our models.
from django.core.exceptions import ValidationError
# This will allow us to search through our string to match our regex function
import re


def validate_name(name):
    error_message = "Improper name format please enter First and Last seperated by a space and with proper capitalization"
    # Message we want to give the user when passing incorrect input
    regex = r'^[A-Z][a-z]+( [A-Z][a-z]+)*$'
    # ^ matches the start of the string.
    # [A-Z] matches a single uppercase letter.
    # [a-z]+ matches one or more lowercase letters.
    # ( [A-Z][a-z]+)* matches zero or more occurrences of a space followed by an uppercase letter and one or more lowercase letters.
    # $ matches the end of the string.
    good_name = re.match(regex, name)
    # returns a boolean value [True || False]
    if good_name:
        return name
    else:
        raise ValidationError(error_message, params={ 'name' : name })