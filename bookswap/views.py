from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Book, SwapRequest 
from .forms import BookForm
 
import requests

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def search_books(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        # Make a request to the Google Books API
        google_books_api_url = f'https://www.googleapis.com/books/v1/volumes?q={search_query}'
        response = requests.get(google_books_api_url)
        if response.status_code == 200:
            # Extract book data from the API response
            books_data = response.json().get('items', [])
            # Process the book data to ensure it matches the template's expectations
            processed_books_data = []
            for item in books_data:
                book_info = item.get('volumeInfo', {})
                book = {
                    'title': book_info.get('title', 'Unknown Title'),
                    'authors': ', '.join(book_info.get('authors', ['Unknown Author'])),
                    'description': book_info.get('description', 'No description available'),
                    'isbn': book_info.get('industryIdentifiers', [{'identifier': 'No ISBN'}])[0]['identifier'],
                    'owner': None  
                }
                processed_books_data.append(book)
            return render(request, 'search_books.html', {'books_data': processed_books_data})
        else:
            error_message = "Failed to fetch books. Please try again later."
            return render(request, 'search_books.html', {'error_message': error_message})
    else:
        return render(request, 'search_books.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def book_list(request):
    books = Book.objects.filter(owner=request.user)
    return render(request, 'book_list.html', {'books': books})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@login_required
def book_detail(request, book_id):
    return render(request, 'book_detail.html')

@login_required
def check_swap_availability(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        # Check if any book instance with the given ISBN is available for swap
        available_books = Book.objects.filter(isbn=isbn).exclude(owner=request.user)
        return render(request, 'swap_availability.html', {'available_books': available_books})
    else:
        return redirect('search_books')  
      
@login_required
def swap_request(request):
    user = request.user
    received_requests = SwapRequest.objects.filter(owner=user)
    sent_requests = SwapRequest.objects.filter(requester=user)
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    return render(request, 'swap_request.html', context)

@login_required
def review_list(request):
    return render(request, 'review_list.html')

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, owner=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, owner=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'delete_book.html', {'book': book})