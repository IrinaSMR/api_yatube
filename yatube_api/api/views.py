from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Comment, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def partial_update(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if request.user == post.author:
            serializer = self.serializer_class(post, data=request.data)
            if serializer.is_valid():
                serializer.save(author=self.request.user, post=post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if request.user == post.author:
            post.delete()
            return Response('Post delete', status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def create(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, post_id, pk):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(self.queryset, id=pk, post=post)
        if request.user == comment.author:
            serializer = self.serializer_class(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(author=self.request.user, post=post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, post_id, pk):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(self.queryset, id=pk, post=post)
        if request.user == comment.author:
            comment.delete()
            return Response(
                'Comment delete',
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(status=status.HTTP_403_FORBIDDEN)
