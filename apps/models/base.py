from django.db.models import Model, DateTimeField, CharField, SlugField, BooleanField
from django.db.models.functions import Now


class TimeBasedModel(Model):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True, db_default=Now())

    class Meta:
        abstract = True


class SlugBasedModel(Model):
    title = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class DeleteBasedModel(Model):
    is_deleted = BooleanField(db_default=False)

    class Meta:
        abstract = True