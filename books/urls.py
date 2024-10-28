from django.urls import path
from books.views import BookListCreate, BookRetrieve, BookUpdate, BookDelete

urlpatterns = [
    path('create/', BookListCreate.as_view(), name='create-book'),
    path('', BookListCreate.as_view(), name='book-list'),
    path('<str:isbn>/', BookRetrieve.as_view(), name='retrieve-book'),
    path('update/<str:isbn>/', BookUpdate.as_view(), name='update-book'),
    path('delete/<str:isbn>/', BookDelete.as_view(), name='delete-book')
]
