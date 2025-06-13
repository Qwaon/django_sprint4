from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Category(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    description = models.TextField("Описание")
    slug = models.SlugField(
        "Идентификатор",
        unique=True,
        help_text=(
            "Используется для формирования URL. Допустимые символы: "
            "латиница, цифры, дефис, подчёркивание."
        )
    )
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        help_text="Отключите, чтобы скрыть категорию."
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField("Название локации", max_length=255)
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        help_text="Отключите, чтобы скрыть локацию."
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата публикации",
        help_text="Можно указать будущую дату для отложенной публикации."
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        verbose_name="Локация",
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        null=True
    )
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        help_text="Отключите, чтобы скрыть публикацию."
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    image = models.ImageField(
        "Изображение", upload_to="post_images", blank=True, null=True
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comments.count() 


class Comments(models.Model):
    text = models.TextField("Комментарий")
    current_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("created_at",)

    @property
    def post_id(self):
        return self.current_post.id 
