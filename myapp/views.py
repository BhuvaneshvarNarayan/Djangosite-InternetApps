from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Review, Member
from .forms import FeedbackForm, SearchForm, OrderForm, ReviewForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.utils import timezone
import random

# Create your views here.
def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    last_login = request.session.get('last_login', 'Your last login was more than one hour ago')
    return render(request, 'myapp/index.html', {'booklist': booklist, 'last_login': last_login})


def about(request):
    # Check for the cookie 'lucky_num'
    if 'lucky_num' in request.COOKIES:
        mynum = request.COOKIES['lucky_num']
    else:
        # Generate a random number between 1 and 100
        mynum = str(random.randint(1, 100))

    # Create a response object
    response = render(request, 'myapp/about.html', {'mynum': mynum})

    # Set the cookie to expire after 5 minutes
    response.set_cookie('lucky_num', mynum, max_age=300)

    return response


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

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            books = form.cleaned_data['books']
            member = order.member
            type = order.order_type
            order.save()
            form.save_m2m()  # This is necessary to save the many-to-many relationship for books
            if type == 1:  # Borrow type
                for b in order.books.all():
                    member.borrowed_books.add(b)
            return render(request, 'myapp/order_response.html', {'books': books, 'order': order})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review = form.save(commit=False)
                review.save()
                book = review.book
                book.num_reviews += 1
                book.save()
                return redirect('myapp:index')  # Redirecting to home
            else:
                form.add_error('rating', 'You must enter a rating between 1 and 5!')
    else:
        form = ReviewForm()

    return render(request, 'myapp/review.html', {'form': form})

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # Generate the date and time of the current login
                request.session['last_login'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                # Set the session expiry to 1 hour
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


@login_required
def chk_reviews(request, book_id):
    user = request.user
    book = get_object_or_404(Book, pk=book_id)

    # Check if the user is a Member
    if hasattr(user, 'member'):
        # User is a Member, calculate the average rating
        reviews = Review.objects.filter(book=book)
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            return render(request, 'myapp/chk_reviews.html', {'book': book, 'average_rating': average_rating})
        else:
            # No reviews found
            message = 'There are no reviews submitted for this book.'
            return render(request, 'myapp/chk_reviews.html', {'book': book, 'message': message})
    else:
        # User is not a Member
        message = 'You are not a registered member!'
        return render(request, 'myapp/chk_reviews.html', {'book': book, 'message': message})
