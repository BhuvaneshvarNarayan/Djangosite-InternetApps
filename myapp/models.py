from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='USA') # Lab 4

    def __str__(self):
        return self.name

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='S')
    num_pages = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True) # Lab 4
    num_reviews = models.PositiveIntegerField(default=0)  # New field

    def __str__(self):
        return self.title

class Member(User):
    STATUS_CHOICES = [
        (1, 'Regular member'),
        (2, 'Premium Member'),
        (3, 'Guest Member'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300, blank=True, null=True) # Lab 4
    city = models.CharField(max_length=20, default='Windsor') # Lab 4
    province=models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField(Book, blank=True)

    class Meta:
        verbose_name = 'Member'

    def __str__(self):
        return self.username

class Order(models.Model):
    PURCHASE = 0
    BORROW = 1
    ORDER_TYPE_CHOICES = [
        (PURCHASE, 'Purchase'),
        (BORROW, 'Borrow'),
    ]

    books = models.ManyToManyField(Book)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    order_type = models.IntegerField(choices=ORDER_TYPE_CHOICES, default=BORROW)
    order_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} by {self.member.username} - {self.get_order_type_display()}"

    def total_items(self):
        return self.books.count()

class Review(models.Model):
    reviewer = models.EmailField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.reviewer} - {self.book.title}"