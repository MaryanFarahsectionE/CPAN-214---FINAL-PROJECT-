from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseForbidden

from .models import Book

def homepage(request):
    books = Book.objects.all()
    context = {
        "bookstore_name": "Bookstore - Trish & Maryan",
        "books": books,
    }
    return render(request, "homepage.html", context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book_detail.html", {"book": book})

@login_required
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        author = request.POST.get("author", "").strip()
        year = request.POST.get("year", "").strip()
        rating = request.POST.get("rating", "").strip()
        description = request.POST.get("description", "").strip()

        errors = []

        if not title:
            errors.append("Title is required.")
        if not author:
            errors.append("Author is required.")
        if not year:
            errors.append("Year is required.")
        elif not year.isdigit():
            errors.append("Year must be a number.")

        if not rating:
            errors.append("Rating is required.")
        else:
            try:
                float(rating)
            except ValueError:
                errors.append("Rating must be a number (e.g. 4.5).")

        if errors:
            return render(request, "add_book.html", {
                "errors": errors,
                "title": title,
                "author": author,
                "year": year,
                "rating": rating,
                "description": description,
            })
        
        book = Book.objects.create(
            title=title,
            author=author,
            year=int(year),
            rating=float(rating),
            description=description,
            posted_by=request.user,
        )

        return redirect("book_detail", book_id=book.id)
    
    return render(request, "add_book.html")

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.posted_by != request.user:
        return HttpResponseForbidden("You can only edit your own books.")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        author = request.POST.get("author", "").strip()
        year = request.POST.get("year", "").strip()
        rating = request.POST.get("rating", "").strip()
        description = request.POST.get("description", "").strip()

        errors = []

        if not title:
            errors.append("Title is required.")
        if not author:
            errors.append("Author is required.")
        if not year:
            errors.append("Year is required.")
        elif not year.isdigit():
            errors.append("Year must be a number.")

        if not rating:
            errors.append("Rating is required.")
        else:
            try:
                float(rating)
            except ValueError:
                errors.append("Rating must be a number (e.g. 4.5).")
        
        if errors:
            return render(request, "edit_book.html", {
                "errors": errors,
                "book": book,
                "title": title,
                "author": author,
                "year": year,
                "rating": rating,
                "description": description,
            })
        
        book.title = title
        book.author = author
        book.year = int(year)
        book.rating = float(rating)
        book.description = description
        book.save()

        return redirect("book_detail", book_id=book.id)
    
    return render(request, "edit_book.html", {"book": book})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.posted_by != request.user:
        return HttpResponseForbidden("You can only delete your own books.")
    
    if request.method == "POST":
        book.delete()
        return redirect("homepage")

    return render(request, "delete_book.html", {"book": book})

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("homepage")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

@login_required
def logout_user(request):
    logout(request)
    return redirect("login")