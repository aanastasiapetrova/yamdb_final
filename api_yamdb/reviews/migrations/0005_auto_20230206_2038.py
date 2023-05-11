# Generated by Django 3.2 on 2023-02-06 16:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("reviews", "0004_alter_title_rating"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Дата добавления"
                    ),
                ),
            ],
            options={
                "ordering": ["pub_date"],
            },
        ),
        migrations.RemoveField(
            model_name="comments",
            name="author",
        ),
        migrations.RemoveField(
            model_name="comments",
            name="review",
        ),
        migrations.AlterModelOptions(
            name="review",
            options={"ordering": ["pub_date"]},
        ),
        migrations.RemoveConstraint(
            model_name="review",
            name="unique_author_title",
        ),
        migrations.AlterField(
            model_name="review",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="pub_date",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, verbose_name="Дата добавления"
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="score",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MaxValueValidator(
                        10, message="Максимальная оценка должна быть не более 10"
                    ),
                    django.core.validators.MinValueValidator(
                        1, message="Минимальная оценка должна быть не менее 1"
                    ),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="text",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="review",
            name="title",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="reviews.title",
            ),
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                fields=("title", "author"), name="unique_review"
            ),
        ),
        migrations.DeleteModel(
            name="Comments",
        ),
        migrations.AddField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="review",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="reviews.review",
            ),
        ),
    ]
