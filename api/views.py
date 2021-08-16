from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from api.models import *
from api.pagination import StandardPostPagination
from api.serializers import *
from rest_framework import viewsets, mixins, status


class PostCommentViewSet(viewsets.ModelViewSet):

    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class PostImageViewSet(viewsets.ModelViewSet):

    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def list(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Post.objects.all().order_by('-created')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = StandardPostPagination
    parser_classes = (MultiPartParser, JSONParser)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'body']
    filterset_fields = ['category', 'title']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_object(self):
        queryset = Post.objects.all()
        obj = queryset.get(pk=self.kwargs['pk'])
        return obj

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostUpdateSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors)

        serializer = PostSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET', 'POST'], detail=True, permission_classes=[IsAuthenticatedOrReadOnly])
    def comments(self, request, pk):
        if request.method == 'GET':
            post = get_object_or_404(Post, id=pk)
            comments = PostComment.objects.filter(post_id=post.id)
            serializer = PostCommentSerializer(comments, many=True)

            return Response(serializer.data)

        if request.method == 'POST':
            instance = self.get_object()
            serializer = PostCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(post=instance)
                return Response(serializer.data)
            return Response(serializer.errors)

    @action(methods=['GET', 'POST'], detail=True, permission_classes=[IsAuthenticatedOrReadOnly],
            parser_classes=(MultiPartParser, JSONParser))
    def images(self, request, pk):
        if request.method == 'GET':
            post = get_object_or_404(Post, id=pk)
            images = PostImage.objects.filter(post_id=post.id)
            serializer = PostImageSerializer(images, many=True)

            return Response(serializer.data)

        if request.method == 'POST':
            instance = self.get_object()
            serializer = PostImageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(post=instance)
                return Response(serializer.data)
            return Response(serializer.errors)

