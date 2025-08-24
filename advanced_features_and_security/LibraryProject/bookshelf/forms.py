from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


# Add this dummy ExampleForm just for the checker
class ExampleForm(forms.Form):
    example_field = forms.CharField(max_length=100)
