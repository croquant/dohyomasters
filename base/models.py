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


N_MONTHS = 12
N_DAYS = 24


class GameDateManager(models.Manager):
    def current(self):
        return self.order_by("year", "month", "day").last()

    def tick(self):
        current_date = self.current()
        if current_date is None:
            self.create(year=1, month=1, day=1)
            return

        year, month, day = (
            current_date.year,
            current_date.month,
            current_date.day,
        )
        day += 1

        if day > N_DAYS:
            day = 1
            month += 1

            if month > N_MONTHS:
                month = 1
                year += 1

        return self.create(year=year, month=month, day=day)


class GameDate(models.Model):
    id = models.SlugField(primary_key=True)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    day = models.PositiveIntegerField()

    objects = GameDateManager()

    def save(self, *args, **kwargs):
        self.id = f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
        super(GameDate, self).save(*args, **kwargs)

    def __str__(self):
        return self.id
