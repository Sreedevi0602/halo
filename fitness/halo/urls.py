from django.urls import path
from .views import class_list_view

urlpatterns = [
    path('classes/', class_list_view, name='class'),
]