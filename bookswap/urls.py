from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search_books/', views.search_books, name='search_books'),
    path('check_swap_availability/', views.check_swap_availability, name='check_swap_availability'),
    path('profile/', views.profile, name='profile'),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('swap_request/', views.swap_request, name='swap_request'),
    path('reviews/', views.review_list, name='review_list'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    
]
