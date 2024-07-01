# myapp/forms.py
from django import forms
from .models import Book
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