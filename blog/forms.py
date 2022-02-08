from django import forms

from .models import Ticket, Review

RATING_OPTIONS = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre'}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {'headline': 'Titre', 'rating': 'Note', 'body': 'Commentaire'}
        widgets = {'rating': forms.RadioSelect(choices=RATING_OPTIONS),
                   'body': forms.Textarea(attrs={'rows': 4})}
