from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from django.urls import include, path

from .views import PostViewSet, GroupViewSet, CommentViewSet

router = DefaultRouter()

router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]