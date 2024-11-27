
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import CharField, BooleanField, BigAutoField, TextField, DateField

from apps.models.managers import CustomUserManager


class User(AbstractUser):
    id = BigAutoField(verbose_name='Telegram id', primary_key=True)
    username = CharField(max_length=255, validators=[UnicodeUsernameValidator()], null=True, blank=True, unique=True)
    email = None
    phone = CharField(max_length=25, unique=True)
    is_online = BooleanField(db_default=False)
    bio = TextField(null=True, blank=True)
    birth_date = DateField(null=True, blank=True)

    objects = CustomUserManager()

    EMAIL_FIELD = ''
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
