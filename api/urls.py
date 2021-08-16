from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import PostViewSet, PostImageViewSet, PostCommentViewSet, CategoryViewSet

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('images', PostImageViewSet)
router.register('comments', PostCommentViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
