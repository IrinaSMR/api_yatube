from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments
        
    def create(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, pk_comment):
        post = get_object_or_404(Post, id=pk)
        comment = get_object_or_404(self.queryset, id=pk_comment, post=pk)
        serializer = self.serializer_class(comment, data=request.data)
        if request.user == comment.author:
            if serializer.is_valid():
                serializer.save(author=self.request.user, post=post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk, pk_comment):
        comment = get_object_or_404(self.queryset, id=pk_comment, post=pk)
        if request.user == comment.author:
            comment.delete()
            return Response('Comment delete', status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
