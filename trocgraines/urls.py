from trocgraines import views
from django.urls import path

app_name = 'trocgraines'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path(
        'legal_disclaimers',
        views.legal_disclaimers,
        name='legal_disclaimers'
        ),
]
