from django import forms
from .models import Blog, BlogImage


# Custom Multiple FileInput widget
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class BlogForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
