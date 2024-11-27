
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.views import room, index, UserListAPIView, AttachmentCreateAPIView, AttachmentRetrivAPIView

urlpatterns = [
    path("", index, name="index"),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('users', UserListAPIView.as_view(), name='attachment'),
    path('attachments', AttachmentCreateAPIView.as_view(), name='attachment'),
    path('attachment/<int:pk>', AttachmentRetrivAPIView.as_view(), name='attachment'),
    path("chat/", room, name="room")
]
