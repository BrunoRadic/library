from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Author, Book, Genre


@login_required
def book_list(request):
    books = Book.objects.select_related('author').prefetch_related('genres').all()

    title = request.GET.get('title', '').strip()
    author = request.GET.get('author', '').strip()
    genre = request.GET.get('genre', '').strip()

    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__last_name__icontains=author)
    if genre:
        books = books.filter(genres__id=genre)

    return render(request, 'books/book_list.html', {
        'books': books,
        'authors': Author.objects.all(),
        'genres': Genre.objects.all(),
    })
