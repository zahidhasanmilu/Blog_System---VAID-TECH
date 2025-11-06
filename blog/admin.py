from django.contrib import admin
from .models import Category, Tag, Blog, BlogImage


# -----------------------
# Inline for Blog Images
# -----------------------
class BlogImageInline(
    admin.TabularInline
):  # চাইলে admin.StackedInline ব্যবহার করতে পারো
    model = BlogImage
    extra = 1  # নতুন Blog বানানোর সময় default 1টা image field দেখাবে


# -----------------------
# Category Admin
# -----------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    readonly_fields = ("slug",)


# -----------------------
# Tag Admin
# -----------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    readonly_fields = ("slug",)


# -----------------------
# Blog Admin
# -----------------------
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "created_date", "slug")
    search_fields = ("title", "author__username")
    list_filter = ("category", "tags", "created_date")
    readonly_fields = ("slug",)
    filter_horizontal = ("tags",)
    inlines = [BlogImageInline]  # ✅ Blog এর সাথে BlogImage inline


# -----------------------
# Blog Image Admin
# -----------------------
@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ("blog", "image")
    search_fields = ("blog__title",)
