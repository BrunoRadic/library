from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm
from .models import Author, Book, Genre


def _is_admin(user):
    return user.groups.filter(name='administrator').exists()


def _is_employee(user):
    return user.groups.filter(name='employee').exists()


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
def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related('author').prefetch_related('genres'), pk=pk)
    return render(request, 'books/book_detail.html', {
        'book': book,
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


@login_required
def user_list(request):
    if not _is_admin(request.user):
        return HttpResponseForbidden()

    role = request.GET.get('role', '').strip()
    users = User.objects.prefetch_related('groups').order_by('username')

    if role:
        users = users.filter(groups__name=role)

    return render(request, 'books/user_list.html', {
        'users': users,
        'groups': Group.objects.all(),
        'selected_role': role,
    })


@login_required
def stats_view(request):
    if not (_is_admin(request.user) or _is_employee(request.user)):
        return HttpResponseForbidden()

    top_genre = (
        Genre.objects.annotate(book_count=Count('book'))
        .order_by('-book_count')
        .first()
    )

    return render(request, 'books/stats.html', {
        'total_books': Book.objects.count(),
        'total_genres': Genre.objects.count(),
        'total_authors': Author.objects.count(),
        'total_users': User.objects.count(),
        'top_genre': top_genre,
    })
