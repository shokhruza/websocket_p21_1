from rest_framework.serializers import ModelSerializer

from apps.models import Attachment, User


class AttachmentModelSerializer(ModelSerializer):
    class Meta:
        model = Attachment
        fields = 'id', 'file'


        # extra_kwargs = {
        #     'file': {'write_only': True},
        # }


class AttachmentDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'


class UserDetailModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'first_name', 'last_name', 'username', 'is_online'