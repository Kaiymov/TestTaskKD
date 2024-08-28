from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny


from account_api.models import Post, Rating, Comment, CustomUser
from account_api.serializers import PostSerializer, CommentSerializer, RatingSerializer, CustomUserSerializer
from .permissions import IsAuthorOrStaff
from .management.commands import bot

class UsersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny,]


class PostAddView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        queryset = CustomUser.objects.filter(id=user.id).values('telegram_chat_id')
        chat_id = queryset.first()['telegram_chat_id']
        print(chat_id)
        message = f"Ваш пост был успешно опубликован!"
        bot.send_telegram_message(chat_id, message)


class PostDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrStaff,]

class PostRetrieveView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentAddView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        post = generics.get_object_or_404(Post, id=self.kwargs['post_id'])
        user = self.request.user
        if user.is_authenticated:
            serializer.save(post=post, author=user)
        else:
            temporary_username = self.request.data.get('temporary_username', 'Anonymous')
            serializer.save(post=post, temporary_username=temporary_username)


class CommentDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrStaff,]


class CommectListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        comment_queryset = Comment.objects.filter(post_id=post_id)
        return comment_queryset


class RatingAddView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        post = generics.get_object_or_404(Post, id=self.kwargs['post_id'])
        user = self.request.user

        if Rating.objects.filter(post=post, author=user).exists():
            raise serializers.ValidationError('You have already rated this post.')

        serializer.save(author=user, post=post)


class RatingDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthorOrStaff,]

