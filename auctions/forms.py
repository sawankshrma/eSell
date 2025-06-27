from django import forms
from .models import Listing, Bid, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category', 'title', 'description', 'starting_bid', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control-1',
                'placeholder': 'Enter a title',
                'style': 'width: 60%; height: 40px; margin-bottom: 5px; margin-top: 0px;'

            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control-1',
                'rows': 4,
                'placeholder': 'Describe your product...',
                'style': 'width: 90%; height: 120px; margin-bottom: 5px; margin-top: 0px;'
            }),
            'starting_bid': forms.NumberInput(attrs={
                'class': 'form-control-1',
                'placeholder': 'Enter starting bid',
                'style': 'width: 60%;  height: 40px; margin-bottom: 5px; margin-top: 0px;'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control-1',
                'placeholder': 'Image URL (optional)',
                'style': 'width: 100%;  height: 40px; margin-bottom: 5px; margin-top: 0px;'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control-1',
                'style': 'width: 30%;  height: 40px; margin-bottom: 5px; margin-top: 0px;'
            }),
        }

class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        labels = {
            'amount': ''
        }
        widgets = {
            'amount': forms.TextInput(attrs={
                'placeholder': 'Enter the amount..',
                'style' : 'height:70px; border-radius: 15px; width: 100%; padding: 7px; font-size:larger; '
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': ''
        }
        widgets = {
            'text': forms.Textarea(attrs={
                
                'placeholder': 'Add a comment..',
                'style': 'width: 85%; height: 90px; padding : 10px; background-color: transparent; border-radius:20px;'

            }),
        }
