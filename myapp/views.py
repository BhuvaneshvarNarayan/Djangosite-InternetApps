from django.shortcuts import render, get_object_or_404
from .models import Book
from .forms import FeedbackForm, SearchForm
from django.http import HttpResponse


# Create your views here.
def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    # return render(request, 'myapp/index0.html', {'booklist': booklist})
    return render(request, 'myapp/index.html', {'booklist': booklist})


def about(request):
    # return render(request, 'myapp/about0.html')
    return render(request, 'myapp/about.html')


def detail_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # return render(request, 'myapp/detail0.html', {'book': book})
    return render(request, 'myapp/detail.html', {'book': book})

def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = ' to borrow books.'
            elif feedback == 'P':
                choice = ' to purchase books.'
            else:
                choice = ' None.'
            return render(request, 'myapp/fb_results.html', {'choice': choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})


def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data.get('category', '')
            max_price = form.cleaned_data['max_price']

            if category:
                booklist = Book.objects.filter(category=category, price__lte=max_price)
            else:
                booklist = Book.objects.filter(price__lte=max_price)

            return render(request, 'myapp/results.html', {'name': name, 'category': category, 'booklist': booklist, 'max_price': max_price})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})