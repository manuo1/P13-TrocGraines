from django.urls import path

from trocgraines import views

app_name = 'trocgraines'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path(
        'legal_disclaimers', views.legal_disclaimers, name='legal_disclaimers'
    ),
]
