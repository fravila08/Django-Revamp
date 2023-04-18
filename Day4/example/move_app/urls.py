from django.urls import path
from .views import All_moves, Selected_move

urlpatterns = [
    path('', All_moves.as_view(), name='all_moves'),
    path('<str:name>/', Selected_move.as_view(), name='selected_move' )
]
