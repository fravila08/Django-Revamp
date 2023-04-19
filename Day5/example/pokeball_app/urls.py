from django.urls import path, register_converter
from .converters import BallTypeConverter
from .views import Pokeball_Img

# register the converter we created so we could utilize it in our paths
register_converter(BallTypeConverter, 'pokeball')

urlpatterns = [
    # utilize the registered converter to ensure the parameter is valid
    path("<pokeball:ball>/", Pokeball_Img.as_view(), name='pokeball'),
]
