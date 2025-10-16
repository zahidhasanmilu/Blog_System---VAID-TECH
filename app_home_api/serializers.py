from rest_framework import serializers
from app_home.models import Blog, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']
        read_only_fields = ['id', 'slug']
        
# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ['id', 'title', 'slug']
#         read_only_fields = ['id', 'slug']

class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    slug = serializers.CharField(read_only=True)

    #create() → new Category create করে
    def create(self, validated_data):
        return Tag.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance

#-------------------------------------------------------------------------------
#----------------------BLOG SERIALIZER------------------------------------------------
#-------------------------------------------------------------------------------

class BlogSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()   # Category model-এর __str__() return হবে
    author = serializers.StringRelatedField()     # Author model-এর __str__() return হবে
    tags = serializers.StringRelatedField(many=True)  # প্রতিটা tag-এর নাম দেখাবে
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'content', 'author', 'category', 'tags', 'created_date', 'created_date']
        read_only_fields = ['id', 'slug', 'created_date', 'created_date']
        
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value
    
    def validate_content(self, value):
        if len(value) < 20:
            raise serializers.ValidationError("Content must be at least 20 characters long.")
        return value
    