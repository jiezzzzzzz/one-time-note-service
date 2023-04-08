from django.urls import path
from .views import index, question, decrypt

urlpatterns = [
    path('', index, name='start_page'),
    path('<int:random_number>/<str:str_key>/', question, name='question'),
    path('/decrypt/<int:random_number>/<str:str_key>', decrypt, name='decrypt')
]