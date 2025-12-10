from django.urls import path
from . import views
from .api import views as api_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('api/books/', api_views.get_books, name='api_get_books'),
    path('api/books/<int:book_id>/', api_views.get_book, name='api_get_book'),
]