from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.alpha_id import alpha_id


class AlphaIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 16)
        kwargs.setdefault("unique", True)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            value = alpha_id()
            setattr(model_instance, self.attname, value)
        return value


class User(AbstractUser):
    id = AlphaIDField(primary_key=True)
    first_name = None
    last_name = None


class GameMonthManager(models.Manager):
    def tick(self):
        current_month = self.order_by("year", "number").last()
        if current_month is None:
            self.create(year=1, number=1)
            return

        year = current_month.year
        month = current_month.number

        if current_month.number == 12:
            year += 1
            month = 1
        else:
            month += 1

        self.create(year=year, number=month)


class GameMonth(models.Model):
    id = models.SlugField(primary_key=True)
    year = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    objects = GameMonthManager()

    def save(self, *args, **kwargs):
        self.id = f"{self.year}-{self.number}"
        super(GameMonth, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.year:04d}-{self.number:02d}"
