# myapp/forms.py
from django import forms
from .models import Book, Order, Review
class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices=FEEDBACK_CHOICES)

class SearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label='Your Name')
    CATEGORY_CHOICES = [
        ('S', 'Science & Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other'),
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label='Select a category:', widget=forms.RadioSelect)
    max_price = forms.IntegerField(label='Maximum Price', min_value=0)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {
            'books': forms.CheckboxSelectMultiple(),
            'order_type': forms.RadioSelect
        }
        labels = {
            'member': 'Member name',
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {
            'book': forms.RadioSelect(),
        }
        labels = {
            'reviewer': 'Please enter a valid email',
            'rating': 'Rating: An integer between 1 (worst) and 5 (best)',
        }