class IntOrStrConverter:
    # The regex attribute is a regular expression that matches any sequence of digits or alphabetic characters. 
    # It is used by Django to match URL patterns against incoming URLs.
    regex = '[0-9]+|[a-zA-Z]+'
    # The to_python method is called by Django when it matches a URL pattern that uses 
    # this converter. It takes the matched string as input and returns the converted value. 
    def to_python(self, value):
        if value.isdigit():
            return int(value)
        else:
            return str(value)
    # The to_url method is called by Django when it generates URLs that use this converter. It takes 
    # the converted value as input and returns a string that can be used in a URL.
    def to_url(self, value):
        return str(value)



