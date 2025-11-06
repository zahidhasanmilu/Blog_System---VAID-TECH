import os
import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# Celery task import
from .tasks import send_new_post_notification_email



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
        if not self.slug:  # only generate slug if it doesn't exist
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


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
        settings.AUTH_USER_MODEL, related_name='user_blogs', on_delete=models.CASCADE
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
    is_published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_date']
        indexes = [models.Index(fields=['title','created_date'])]
        
    # def save(self, *args, **kwargs):
    #     base_slug = slugify(self.title)
    #     if not self.slug:
    #         self.slug = generate_unique_slug(Blog, base_slug)
    #     return super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # ----------------------------------------------------
        # 1. Initial Data for Celery Trigger and Slug Logic
        # ----------------------------------------------------
        
        # Check if the instance is new (PK is None)
        is_new = self.pk is None 
        # Get the previous publish status before saving
        old_is_published = False
        
        if not is_new:
            try:
                # Fetch the previous status from the database
                old_is_published = Blog.objects.get(pk=self.pk).is_published
            except Blog.DoesNotExist:
                pass 

        # ----------------------------------------------------
        # 2. Slug Generation Logic
        # ----------------------------------------------------
        base_slug = slugify(self.title)

        if not self.slug or (self.pk and Blog.objects.get(pk=self.pk).title != self.title):
            # Generate a new slug if it's a new object OR the title has been changed
            self.slug = generate_unique_slug(Blog, base_slug)

        # ----------------------------------------------------
        # 3. Perform the main save operation first
        # ----------------------------------------------------
        super().save(*args, **kwargs) # Save the post to the database

        # ----------------------------------------------------
        # 4. Celery Task Calling Logic
        # ----------------------------------------------------
        
        # Condition Check: 
        # 1. The post must currently be published (self.is_published == True)
        # AND 
        # 2. It must be either a new post (is_new == True) 
        #    OR it must have just changed from 'Draft' (False) to 'Published' (True)
        
        if self.is_published and (is_new or not old_is_published):
            # Call the Celery task
            # .delay() sends the task asynchronously to the Redis queue
            post_url = self.get_absolute_url()
            send_new_post_notification_email.delay(self.title, post_url) 
            print(f"Celery: New post notification task added for: {self.title}")

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
