from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объекта класса User."""
    class Meta:
        model = User
        fields = ("username", "email")

    def validate(self, data):
        """Запрещает пользователям присваивать себе имя me
        и использовать повторные username и email."""
        if data.get("username") == "me":
            raise serializers.ValidationError("Использовать имя me запрещено")
        if User.objects.filter(username=data.get("username")):
            raise serializers.ValidationError(
                "Пользователь с таким username уже существует"
            )
        if User.objects.filter(email=data.get("email")):
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует"
            )
        return data


class UserRecieveTokenSerializer(serializers.Serializer):
    """Сериализатор для объекта класса User при получении токена JWT."""
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )
    confirmation_code = serializers.CharField(max_length=150, required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    def validate_username(self, username):
        if username in "me":
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено')
        return username


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов класса Genre"""
    class Meta:
        exclude = ("id",)
        model = Genre
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для объектов класса Category"""
    class Meta:
        exclude = ("id",)
        model = Category
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class TitleForGETSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов класса Title для обработки GET-запросов"""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ("id",
                  "name",
                  "year",
                  "rating",
                  "description",
                  "genre",
                  "category")


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов класса Title
    для обработки небезопасных запросов"""
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        fields = ("id",
                  "name",
                  "year",
                  "description",
                  "genre",
                  "category")
        model = Title

    def to_representation(self, instance):
        serializer = TitleForGETSerializer(instance)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов класса Review"""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            "id",
            "text",
            "author",
            "score",
            "pub_date",
        )

    def validate(self, data):
        if self.context["request"].method == "POST":
            title_id = self.context["view"].kwargs.get("title_id")
            author = self.context["request"].user
            if Review.objects.filter(author=author, title=title_id).exists():
                raise serializers.ValidationError(
                    "Вы уже написали отзыв к этому произведению."
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов класса Comment"""
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field="username")

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
