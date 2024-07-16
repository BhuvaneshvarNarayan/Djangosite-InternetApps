from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review

# Register your models here.
admin.site.register(Publisher)

class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price')]
    list_display = ('title', 'category', 'price')

# Register the Book model with BookAdmin
admin.site.register(Book, BookAdmin)

class OrderAdmin(admin.ModelAdmin):
    fields = [('books'), ('member', 'order_type', 'order_date')]
    list_display = ('id', 'member', 'order_type', 'order_date', 'total_items')

# Register the Order model with OrderAdmin
admin.site.register(Order, OrderAdmin)

# Register the Member model
admin.site.register(Member)

# Register the Review model
admin.site.register(Review)