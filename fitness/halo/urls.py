from django.urls import path
from .views import class_list_view, book_class, get_bookings

urlpatterns = [
    path('classes/', class_list_view, name='class'),
    path('book/', book_class, name='book_class'),
    path('bookings/', get_bookings, name='get_bookings'),
]