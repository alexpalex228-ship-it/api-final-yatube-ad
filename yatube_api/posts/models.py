from django.contrib.auth import get_user_model
from django.core.validators import validate_slug
from django.db import models
from django.utils.translation import gettext_lazy as _

from posts.constants import POST_STR_LENGTH

User = get_user_model()


class Group(models.Model):
    """Модель группы для объединения постов."""

    title = models.CharField(
        max_length=200,
        verbose_name=_('Название'),
        help_text=_('Название группы (максимум 200 символов)')
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[validate_slug],
        verbose_name=_('Уникальный идентификатор'),
        help_text=_('Уникальный идентификатор группы в URL')
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        help_text=_('Подробное описание группы')
    )

    class Meta:
        verbose_name = _('Группа')
        verbose_name_plural = _('Группы')

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель поста пользователя."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('Автор'),
        help_text=_('Автор публикации')
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name=_('Группа'),
        help_text=_('Группа, к которой относится публикация')
    )
    text = models.TextField(
        verbose_name=_('Текст'),
        help_text=_('Текст публикации')
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата публикации'),
        help_text=_('Дата и время создания публикации')
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name=_('Изображение'),
        help_text=_('Изображение для публикации')
    )

    class Meta:
        verbose_name = _('Публикация')
        verbose_name_plural = _('Публикации')
        ordering = ['-pub_date']
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:POST_STR_LENGTH]


class Comment(models.Model):
    """Модель комментария к посту."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Автор'),
        help_text=_('Автор комментария')
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Публикация'),
        help_text=_('Публикация, к которой относится комментарий')
    )
    text = models.TextField(
        verbose_name=_('Текст'),
        help_text=_('Текст комментария')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Дата создания'),
        help_text=_('Дата и время создания комментария')
    )

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')
        ordering = ['-created']
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:POST_STR_LENGTH]


class Follow(models.Model):
    """Модель подписки на пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name=_('Подписчик'),
        help_text=_('Пользователь, который подписывается')
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_('Автор'),
        help_text=_('Пользователь, на которого подписываются')
    )

    class Meta:
        verbose_name = _('Подписка')
        verbose_name_plural = _('Подписки')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='prevent_self_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
