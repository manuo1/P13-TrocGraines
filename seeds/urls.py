from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import CreateSeedView

app_name = 'seeds'

urlpatterns = [
    path(
        'add_seed/',
        CreateSeedView.as_view(),
        name='add_seed'
    ),
    path(
        'my_seeds/',
        views.my_seeds,
        name='my_seeds'
    ),
]
