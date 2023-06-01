from django import forms
from .models import *


class AddReviewForm(forms.Form):
    estimation = forms.IntegerField(max_value=5, min_value=1, label='Оценка')
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Коментарий')
