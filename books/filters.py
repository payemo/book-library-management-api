import django_filters
from books.models import Book

class BookFilter(django_filters.FilterSet):
    published_year = django_filters.NumberFilter(field_name='published_date', lookup_expr='year')
    published_year__gt = django_filters.NumberFilter(field_name='published_date', lookup_expr='year__gt')
    published_year__lt = django_filters.NumberFilter(field_name='published_date', lookup_expr='year__lt')

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains')
        
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'language']
        unknown_field_behavior = django_filters.UnknownFieldBehavior.WARN
