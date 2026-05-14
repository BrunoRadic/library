from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm
from .models import Author, Book, Genre


def _is_admin(user):
    return user.groups.filter(name='administrator').exists()


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
        'is_admin': _is_admin(request.user),
    })


@login_required
def book_add(request):
    if not _is_admin(request.user):
        return HttpResponseForbidden()

    form = BookForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('book_list')

    return render(request, 'books/book_form.html', {'form': form, 'book': None})


@login_required
def book_edit(request, pk):
    if not _is_admin(request.user):
        return HttpResponseForbidden()

    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('book_list')

    return render(request, 'books/book_form.html', {'form': form, 'book': book})
