import random

from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField

from base.models import AlphaIDField, GameDate, User

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

    debut = models.ForeignKey(
        GameDate,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="debut",
    )
    intai = models.ForeignKey(
        GameDate,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="intai",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Rikishi"


class RikishiStats(models.Model):
    rikishi = models.OneToOneField(
        Rikishi,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="stats",
    )

    potential = models.PositiveIntegerField()
    xp = models.PositiveIntegerField(default=0)

    strength = models.PositiveIntegerField(default=1)
    technique = models.PositiveIntegerField(default=1)
    balance = models.PositiveIntegerField(default=1)
    endurance = models.PositiveIntegerField(default=1)
    mental = models.PositiveIntegerField(default=1)

    @property
    def current(self):
        return (
            self.strength
            + self.technique
            + self.balance
            + self.endurance
            + self.mental
        )

    def __str__(self):
        return (
            f"Potential: {self.current}/{self.potential}\n"
            f"XP: {self.xp}\n"
            f"Strength: {self.strength}\n"
            f"Technique: {self.technique}\n"
            f"Balance: {self.balance}\n"
            f"Endurance: {self.endurance}\n"
            f"Mental: {self.mental}"
        )

    def increase_random_stats(self, amount: int = 1):
        while amount > 0 and self.current < self.potential:
            stats = ["strength", "technique", "balance", "endurance", "mental"]
            random_stat = random.choice(stats)
            current_value = getattr(self, random_stat)
            if current_value < 20:
                setattr(self, random_stat, current_value + 1)
                amount -= 1
