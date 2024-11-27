from django.db.models import Q
from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView

from apps.models import Attachment, User, Message
from apps.serializers import AttachmentModelSerializer, AttachmentDetailModelSerializer, UserDetailModelSerializer


# Create your views here.
def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailModelSerializer
    filter_backends = [SearchFilter]
    search_fields = 'username', 'first_name'

    def get_queryset(self):
        user = self.request.user
        user_ids = Message.objects.filter(Q(to_user=user) | Q(from_user=user)).values_list('to_user_id', 'from_user_id').distinct()
        user_ids = set(sum(user_ids, ()))
        user_ids.discard(user.id)
        return super().get_queryset().filter(id__in=user_ids)


class AttachmentCreateAPIView(CreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentModelSerializer


class AttachmentRetrivAPIView(RetrieveAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentDetailModelSerializer