from rest_framework import serializers

# TODO (Maryan): make sure Book model exists in books/models.py
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "year", "rating", "description"]