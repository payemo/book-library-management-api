from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Book
from datetime import date

def generate_isbn13():
    import random
    
    base_digits = [random.randint(0, 9) for _ in range(12)]
    
    total = 0
    for i, digit in enumerate(base_digits):
        if i % 2 == 0:
            total += digit
        else:
            total += digit * 3
    
    check_digit = (10 - (total % 10)) % 10

    isbn13 = ''.join(map(str, base_digits)) + str(check_digit)
    return isbn13

class BookTests(APITestCase):
    def setUp(self):
        number_of_books = 10

        # Create books for testing pagination
        for id in range(number_of_books):
            Book.objects.create(
                title=f'Book {id}',
                author=f'Author {id}',
                isbn=generate_isbn13(),
                language='gbr'
            )
        
        # Create couple of books for a field-specific testing.
        self.book1 = Book.objects.create(
            title='Test book',
            author='Anonymous',
            published_date=date(2024, 10, 28),
            isbn='9786472804704',
            pages=100,
            language='ukr'
        )
        self.book2 = Book.objects.create(
            title='Test book 2',
            author='Anonymous 2',
            published_date=date(2024, 10, 28),
            isbn='9786472804712',
            pages=150,
            language='eng'
        )

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # pagination
        self.assertEqual(response.data['count'], 12)
        self.assertEqual(len(response.data['results']), 10)

    def test_pagination(self):
        url = reverse('book-list') + '?page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 12)
        self.assertEqual(len(response.data['results']), 10)

        url = url.replace('?page=1', '?page=2')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 12)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_create_book(self):
        url = reverse('create-book')
        data = {
            'isbn': '9781318665174',
            'title': 'Test Book (create)',
            'author': 'Anonymous Author 3',
            'published_date': '2024-10-29',
            'language': 'fra'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 13)

    def test_retrive_book(self):
        url = reverse('retrieve-book', args=[self.book1.isbn])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['isbn'], self.book1.isbn)

    def test_filter_by_author(self):
        url = reverse('book-list') + '?author=Anonymous'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['isbn'], self.book1.isbn)
        self.assertEqual(response.data['results'][1]['isbn'], self.book2.isbn)

    def test_filter_by_title(self):
        url = reverse('book-list') + '?title=Test Book 2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], self.book2.title)

    def test_filter_by_published_date(self):
        url = reverse('book-list') + '?published_date=2024-10-28'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['published_date'], self.book1.published_date.strftime('%Y-%m-%d'))
        self.assertEqual(response.data['results'][1]['published_date'], self.book2.published_date.strftime('%Y-%m-%d'))

    def test_filter_by_language(self):
        url = reverse('book-list') + '?language=eng'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['isbn'], self.book2.isbn)

    def test_update_book(self):
        url = reverse('update-book', args=[self.book1.isbn])
        data = {'language': 'eng'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.language, 'eng')

    def test_delete_book(self):
        url = reverse('delete-book', args=[self.book2.isbn])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 11)
        
        
        
