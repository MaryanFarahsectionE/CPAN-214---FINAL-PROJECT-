from rest_framework.decorators import api_view
from rest_framework.response import Response

# TODO (Maryan): ensure Book model exists in books/models.py
from books.models import Book
from .serializers import BookSerializer

@api_view(["GET"])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found"}, status=404)

    serializer = BookSerializer(book)
    return Response(serializer.data)