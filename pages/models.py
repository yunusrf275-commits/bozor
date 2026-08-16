

from django.db import models
from django.utils.text import slugify


class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL (латиницей)")
    content = models.TextField(verbose_name="Содержимое")
    is_published = models.BooleanField(default=True, verbose_name="Опубликована")
    show_in_footer = models.BooleanField(default=True, verbose_name="Показывать в футере")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок в футере")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
