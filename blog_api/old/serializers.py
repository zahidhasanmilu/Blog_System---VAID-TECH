from rest_framework import serializers
from app_home.models import Blog, Category, Tag


# -------------------------------------------------------------------------------
# ----------------------BLOG SERIALIZER------------------------------------------------
# -------------------------------------------------------------------------------
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogSerializer(serializers.ModelSerializer):
    # Readable name
    category_name = serializers.StringRelatedField(source="category", read_only=True)
    tag_names = serializers.StringRelatedField(source="tags", many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    # Writable IDs
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "author",
            "category",
            "category_name",
            "tags",
            "tag_names",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["id", "slug", "author", "created_date", "updated_date"]

    # Validation methods
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long."
            )
        return value

    def validate_content(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(
                "Content must be at least 20 characters long."
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    category_blogs = BlogSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "title", "slug", "category_blogs"]
        read_only_fields = ["id", "slug"]


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ['id', 'title', 'slug']
#         read_only_fields = ['id', 'slug']


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    slug = serializers.CharField(read_only=True)

    # create() → new Category create করে
    def create(self, validated_data):
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.save()
        return instance
