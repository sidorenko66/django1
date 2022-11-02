from django.shortcuts import render, redirect

from books.converters import PubDateConverter
from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    context = {'books': Book.objects.all()}
    return render(request, template, context)

def books_date_view(request, year, month, day):
    template = 'books/books_list.html'
    prev = Book.objects.filter(pub_date__lt=f'{year}-{month}-{day}').order_by('-pub_date')[:1]
    prev = str(prev[0].pub_date) if prev else False
    print(prev)
    next = Book.objects.filter(pub_date__gt=f'{year}-{month}-{day}').order_by('pub_date')[:1]
    next = str(next[0].pub_date) if next else False
    print(next)
    context = {'books': Book.objects.filter(pub_date=f'{year}-{month}-{day}'), 'prev': prev, 'next': next}
    return render(request, template, context)