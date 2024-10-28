from django.shortcuts import render
from rest_framework import generics
from django_filters import rest_framework as filters
from books.models import Book
from books.serializers import BookSerializer
from books.filters import BookFilter

class BookListCreate(generics.ListCreateAPIView):
    """
    API endpoint that allows both creation and listing books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.DjangoFilterBackend,]
    filterset_class = BookFilter

class BookRetrieve(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a book by a specified 'isbn' key.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'isbn'

class BookUpdate(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving or updating a book by a specified 'isbn' key.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'isbn'

    # Note: By setting partial=True, we're allowing partial updates even with PUT requests.
    # However, this deviates from REST conventions, where PUT is typically used for full updates.
    
    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs, partial=True)
        

class BookDelete(generics.RetrieveDestroyAPIView):
    """
    API endpoint for retrieving or deleting a book by a specified 'isbn' key.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'isbn'
