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
