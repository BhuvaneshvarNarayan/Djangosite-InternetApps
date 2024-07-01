# Import necessary classes
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from .models import Publisher, Book


# Create your views here.
def index(request):
    response = HttpResponse()

    # Query all books ordered by primary key
    booklist = Book.objects.all().order_by('id')
    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>' + str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    # Query all publishers sorted by city in descending order
    publisher_list = Publisher.objects.all().order_by('-city')
    heading2 = '<p>' + 'List of publishers: ' + '</p>'
    response.write(heading2)
    for publisher in publisher_list:
        para = '<p>' + publisher.name + ' (' + publisher.city + ')</p>'
        response.write(para)

    return response

def about(request):
    # Create an HTTP response with the desired text
    about_text = "This is an eBook APP."
    return HttpResponse(about_text)


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    response = HttpResponse()
    title = book.title.upper()
    price = f"${book.price}"
    publisher = book.publisher.name

    response.write(f"<p>Title: {title}</p>")
    response.write(f"<p>Price: {price}</p>")
    response.write(f"<p>Publisher: {publisher}</p>")

    return response

def publisher(request):
    response = "Text"
    publisher = Publisher(name="BhuvaneshvarNarayan", city="Windsor", country="Canada", website="www.uwindsor.ca")
    publisher.save()
    return HttpResponse(response)

def price_update(request, book_id):
    book = Book.objects.get(pk=3)
    new_price = '$65'
    book.price = new_price
    book.save()

def update_pub_name(request):
    book = Book.objects.get(pk=2)
    pub_new_name = 'Narayan'
    book.publisher.name = pub_new_name
    book.save()