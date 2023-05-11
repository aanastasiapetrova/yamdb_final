from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель Category"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Модель Genre"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Модель Title"""
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
    )

    genre = models.ManyToManyField(Genre, through="TitleGenre")
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class TitleGenre(models.Model):
    """Промежуточная модель TitleGenre"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    """Модель Review"""
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, db_index=True
    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="reviews")
    score = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(
                10, message="Максимальная оценка должна быть не более 10"
            ),
            MinValueValidator(
                1, message="Минимальная оценка должна быть не менее 1"
            ),
        ]
    )
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name="reviews")

    class Meta:
        ordering = ("pub_date",)
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "title",
                    "author",
                ),
                name="unique_review",
            ),
        )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель Comment"""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="comments")
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("pub_date",)

    def __str__(self):
        return self.text
