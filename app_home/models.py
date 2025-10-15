import os
import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


# -----------------------
# Utility Functions
# -----------------------

# Sanitize filename by replacing forbidden characters
def sanitize_filename(filename):
    forbidden = '<>:"/\\|?*'
    trans = str.maketrans({c: '_' for c in forbidden})
    return filename.translate(trans)


# Generate unique slug
def generate_unique_slug(model, base_slug):
    unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
    return unique_slug


# -----------------------
# Models
# -----------------------

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=300)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=300)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Blog(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_blogs',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=300)
    content = RichTextUploadingField()
    category = models.ForeignKey(
        Category,
        related_name='category_blogs',
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(Tag, related_name='tag_blogs')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_date']
        indexes = [models.Index(fields=['title','created_date'])]
        
    def save(self, *args, **kwargs):
        base_slug = slugify(self.title)
        if not self.slug:
            self.slug = generate_unique_slug(Blog, base_slug)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']
        indexes = [models.Index(fields=['title','created_date'])]
        
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'slug': self.slug})


class BlogImage(models.Model):
    blog = models.ForeignKey(
        Blog,
        related_name='blog_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='blog_images/')

    def save(self, *args, **kwargs):
        if self.image:
            base, ext = os.path.splitext(self.image.name)
            filename = sanitize_filename(base)
            self.image.name = f"{filename}_{uuid.uuid4().hex[:6]}{ext}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.blog.title
