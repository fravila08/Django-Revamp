from django.urls import converters

# It's still ensuring it's a string so we don't need regex
class BallTypeConverter(converters.StringConverter):
    # The types of pokeballs we want to be able to accept
    allowed_balls = ['masterball', 'pokeball', 'ultraball', 'greatball']
    # What should Django do when receiving this parameter incorrectly
    def to_python(self, value):
        if value.lower() not in self.allowed_balls:
            raise ValueError('Invalid ball type')
        return value.lower()