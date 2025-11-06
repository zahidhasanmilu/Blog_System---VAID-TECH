from django import forms
from .models import Blog, Tag, Category, BlogImage


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


class BlogForm(forms.ModelForm):
    # Extra field for image (not in Blog model)
    image = forms.ImageField(required=False, help_text="Optional blog image")

    class Meta:
        model = Blog
        fields = ["title", "content", "category", "tags"]  # <--- 'image' বাদ দিতে হবে
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("title"),
            Field("content"),
            Field("category"),
            Field("tags", css_class="d-flex flex-wrap"),  # inline checkbox
            Field("image"),
            Submit("submit", "Update Blog", css_class="btn btn-primary"),
        )
