from django.urls import path

from . import views

app_name = 'exchange_messages'

urlpatterns = [
    path(
        'new_message/<int:seed_id>/<int:owner_id>',
        views.new_message,
        name='new_message',
    ),
    path('my_messages', views.my_messages, name='my_messages'),
]
