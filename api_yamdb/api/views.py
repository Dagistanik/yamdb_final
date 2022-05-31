from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, GenreTitle, Review, Title
from .custom_filters import CategoryFilter
from .mixins import BaseViewSet
from .permissions import AuthorAdminModer, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, MeSerializer,
    ReviewSerializer, SignupUserSerializer, TitleGETSerializer,
    TitleSerializer, TokenSerializer, UsersSerializer,
)
from api.tokens import default_token_generator
from api_yamdb.settings import FROM_EMAIL


User = get_user_model()


@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def send_confirmation_code(request):
    serializer = SignupUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    code = default_token_generator.make_token(serializer.instance)
    send_mail(
        subject='confirmation_code',
        message=(
            f'{serializer.instance.username} your '
            f'confirmation_code: {code}'
        ),
        from_email=FROM_EMAIL,
        recipient_list=(serializer.instance.email,)
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.save()
    user = get_object_or_404(User, username=data['username'])
    user.password = ''
    user.save()
    token = str(AccessToken.for_user(user))
    return Response(
        {'token': token},
        status=status.HTTP_200_OK
    )


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = CategoryFilter
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleGETSerializer
        return TitleSerializer

    def get_queryset(self):
        queryset = Title.objects.all()
        genre = self.request.query_params.get('genre')
        if genre is not None:
            genre = get_object_or_404(Genre, slug=genre)
            title_list = GenreTitle.objects.values_list(
                'title', flat=True).filter(genre_id=genre)

            queryset = Title.objects.filter(id__in=title_list)
        return queryset

    def perform_update(self, serializer):
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        title = serializer.save(category=category)
        title.genre.clear()
        genres_data = self.request.data.get('genre')
        if genres_data is None:
            genres_data = serializer.instance.genre
        for genre_data in genres_data.all():
            genre = get_object_or_404(Genre, slug=genre_data)
            GenreTitle.objects.create(title=title, genre=genre)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UsersSerializer
    lookup_field = 'username'
    lookup_url_kwargs = 'username'
    lookup_value_regex = r'[\w.@+-]+'

    def get_object(self):
        if self.kwargs.get('username', None) == 'me':
            self.kwargs['username'] = self.request.user.username
        return super(UsersViewSet, self).get_object()


class MeViewSet(APIView):

    def get_object(self, username):
        return get_object_or_404(User, username=username)

    def get(self, request):
        user = self.get_object(request.user.username)
        serializer = MeSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = self.get_object(request.user.username)
        serializer = MeSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        AuthorAdminModer,
    )

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModer,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()
