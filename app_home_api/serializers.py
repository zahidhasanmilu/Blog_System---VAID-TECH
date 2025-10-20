from rest_framework import serializers
from app_home.models import Blog, Category, Tag


# -------------------------------------------------------------------------------
# ----------------------BLOG SERIALIZER------------------------------------------------
# -------------------------------------------------------------------------------
from django.contrib.auth import get_user_model
User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']
        read_only_fields = ['id', 'slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title', 'slug']
        read_only_fields = ['id', 'slug']


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'content', 'author',
                  'category', 'tags', 'created_date', 'updated_date']
        read_only_fields = ['id', 'slug', 'created_date', 'updated_date']

        extra_kwargs = {
            'title': {'required': True},
            'error_messages': {
                'title': {
                    'unique': "A blog with this title already exists.",
                },
            },
            'tags': {'required': True},
            'category': {'required': True},
        }
