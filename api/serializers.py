from rest_framework import serializers;

from api.models import PostImage, PostComment, Post, Category


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image')


class PostCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComment
        fields = ('id', 'author', 'body',)


class CategoryInlineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True)
    comments = PostCommentSerializer(many=True)
    category = CategoryInlineSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'created', 'created_by', 'images', 'comments', 'category']


class PostUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
