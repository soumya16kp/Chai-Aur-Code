from django import forms 
from .models import ChaiReview

class ChaiReviewForm(forms.ModelForm):
    class Meta:
        model = ChaiReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Write your review here...'}),
        }
