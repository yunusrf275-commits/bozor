


from django.db import models
from django.utils.text import slugify

from django.core.exceptions import ValidationError


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE,
        verbose_name="Родитель",
    )
    level = models.PositiveSmallIntegerField(verbose_name="Уровень")
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
        ordering = ['level', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Location.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def clean(self):
        if self.level == 1 and self.parent is not None:
            raise ValidationError("У локации уровня 1 не может быть родителя.")
        if self.level > 1:
            if self.parent is None:
                raise ValidationError("Для уровня выше 1 обязательно нужно указать родителя.")
            if self.parent.level != self.level - 1:
                raise ValidationError(
                    f"Родитель должен быть уровня {self.level - 1}, а выбран уровень {self.parent.level}."
                )
        # остальной save() (генерация slug) не трогаем
