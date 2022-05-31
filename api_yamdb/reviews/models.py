from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from api_yamdb.settings import SCORE_MAX, SCORE_MIN

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        help_text='До 256 символов'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug',
        help_text='Установите slug'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name='Название жанра',
        help_text='До 256 символов'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug',
        help_text='Установите slug'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        help_text='До 256 символов'
    )
    year = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(date.today().year),),
        verbose_name='Год',
        help_text='Год'

    )
    description = models.TextField(
        default='', null=True, blank=True,
        verbose_name='Описание',
        help_text='Введите текст'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True,
        verbose_name='категория',
        help_text='выберите категорию'
    )

    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=True,
        verbose_name='Жанр',
        help_text='Установите жанр'
    )

    @property
    def rating(self):
        if not Review.objects.filter(title=self.id).exists():
            return None
        rating = Review.objects.filter(title=self.id).aggregate(
            models.Avg('score')
        )

        return(rating['score__avg'])

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('id',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Описание жанра',
        help_text='Описание'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='Жанр',
        help_text='Установите жанр'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'genre'),
                name='unique_title_genre'
            )
        )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='title',
        help_text='Установите title'
    )
    text = models.TextField(
        null=True,
        blank=True,
        verbose_name='Краткое описание',
        help_text='Введите текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Author',
        help_text='Выберите автора'
    )
    score = models.PositiveIntegerField(
        validators=(
            MaxValueValidator(SCORE_MAX),
            MinValueValidator(SCORE_MIN)
        ),
        verbose_name='Оценка произведения',
        help_text=f'от {SCORE_MIN} до {SCORE_MAX}'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
        help_text='Дата'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            )
        )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Author',
        help_text='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='reviews',
        help_text='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
        help_text='Дата'
    )
    text = models.TextField(
        null=True,
        blank=True,
        verbose_name='text',
        help_text='Teкст')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
