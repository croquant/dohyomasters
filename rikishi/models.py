from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField

from base.models import AlphaIDField, User

from .constants import (
    DIRECTION_NAMES,
    DIRECTION_NAMES_SHORT,
    DIVISION_NAMES,
    DIVISION_NAMES_SHORT,
    JAPAN_PREFECTURES,
    RANK_NAMES,
    RANK_NAMES_SHORT,
    RANKING_LEVELS,
)


class Division(models.Model):
    slug = models.SlugField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=12,
        choices=DIVISION_NAMES,
    )
    level = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Division, self).save(*args, **kwargs)

    def short_name(self):
        return DIVISION_NAMES_SHORT[self.name]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["level"]


class Rank(models.Model):
    slug = models.SlugField(
        primary_key=True,
    )
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name="ranks",
    )
    title = models.CharField(
        max_length=12,
        choices=RANK_NAMES,
    )
    level = models.PositiveSmallIntegerField()
    order = models.PositiveSmallIntegerField(
        blank=True,
        default=0,
    )
    direction = models.CharField(
        max_length=4,
        choices=DIRECTION_NAMES,
        blank=True,
    )

    def name(self):
        if self.order and self.direction:
            dir_shorthand = DIRECTION_NAMES_SHORT[self.direction]
            return f"{self.title} {self.order}{dir_shorthand}"
        else:
            return self.title

    def long_name(self):
        if self.order and self.direction:
            return f"{self.title} {self.order} {self.direction}"
        else:
            return self.title

    def short_name(self):
        shorthand = RANK_NAMES_SHORT[self.title]
        if self.order and self.direction:
            dir_shorthand = DIRECTION_NAMES_SHORT[self.direction]
            return f"{shorthand}{self.order}{dir_shorthand}"
        else:
            return shorthand

    def save(self, *args, **kwargs):
        self.slug = slugify(self.short_name())
        if Division.objects.filter(name=self.title).exists():
            self.division = Division.objects.get(name=self.title)
        else:
            self.division = Division.objects.get(name="Makuuchi")
        self.level = RANKING_LEVELS[self.title]
        super(Rank, self).save(*args, **kwargs)

    def __str__(self):
        return self.name()

    class Meta:
        ordering = ["level", "order", "direction"]


class Heya(models.Model):
    id = AlphaIDField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    name_jp = models.CharField(max_length=32, unique=True)
    master = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="heya"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Heya"


class Shusshin(models.Model):
    slug = models.SlugField(
        primary_key=True,
    )
    country = CountryField(default="JP")
    prefecture = models.CharField(
        choices=JAPAN_PREFECTURES,
        max_length=32,
        default=None,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if self.country == "JP":
            self.slug = slugify(self.prefecture)
        else:
            self.slug = slugify(self.country.name)
        super(Shusshin, self).save(*args, **kwargs)

    def __str__(self):
        if self.country == "JP":
            return self.prefecture
        else:
            return self.country.name

    class Meta:
        ordering = ["country", "prefecture"]
        verbose_name_plural = "Shusshin"


class Rikishi(models.Model):
    id = AlphaIDField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    name_jp = models.CharField(max_length=64, unique=True)

    shusshin = models.ForeignKey(
        Shusshin,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="rikishi",
    )
    heya = models.ForeignKey(
        Heya,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="rikishi",
    )
    rank = models.ForeignKey(
        Rank,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="rikishi",
    )

    birth_date = models.DateField()
    debut = models.DateField(blank=True, null=True)
    intai = models.DateField(blank=True, null=True)

    height = models.DecimalField(max_digits=4, decimal_places=1)
    weight = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Rikishi"
