from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import ForeignKey, CASCADE, FileField, CharField, ManyToManyField, TextChoices, TextField, \
    PositiveIntegerField, SET_NULL

from apps.models.base import TimeBasedModel


class Attachment(TimeBasedModel):
    file = FileField(upload_to='attachments/%Y/%m/%d/')


class Chat(TimeBasedModel):
    class Type(TextChoices):
        CHANNEL = 'channel', 'Channel'
        GROUP = 'group', 'Group'
        PRIVATE = 'private', 'Private'

    name = CharField(max_length=128)
    type = CharField(max_length=25, choices=Type.choices)
    info = TextField(null=True, blank=True)
    username = CharField(max_length=255, unique=True, null=True, blank=True, validators=[UnicodeUsernameValidator()])
    online_count = PositiveIntegerField(verbose_name='Onlaynlar soni', db_default=0)
    owner = ForeignKey('apps.User', SET_NULL, null=True, blank=True, related_name='chats')
    members = ManyToManyField('apps.User', blank=True)

    def join(self, user):
        self.members.add(user)
        self.save()

    def leave(self, user):
        self.members.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.owner.phone})'


class Message(TimeBasedModel):
    from_user = ForeignKey('apps.User', CASCADE, related_name='from_messages')
    to_user = ForeignKey('apps.User', CASCADE, related_name='to_messages')
    text = CharField(max_length=1024)

    def __str__(self):
        return f'{self.from_user_id}->{self.to_user_id} {self.text} [{self.created_at}]'