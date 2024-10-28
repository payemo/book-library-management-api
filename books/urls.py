from django.urls import path
from books.views import BookList, BookCreate, BookRetrieve, BookUpdate, BookDelete

urlpatterns = [
    path('create/', BookCreate.as_view(), name='create-book'),
    path('', BookList.as_view(), name='book-list'),
    path('<str:isbn>/', BookRetrieve.as_view(), name='retrieve-book'),
    path('update/<str:isbn>/', BookUpdate.as_view(), name='update-book'),
    path('delete/<str:isbn>/', BookDelete.as_view(), name='delete-book')
]
