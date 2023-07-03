from rest_framework.permissions import IsAuthenticated

from utils.util import ResponseModelViewSet
from .models import UserEnquiry
from .serializers import EnquirySerializers


class EnquiryViewSet(ResponseModelViewSet):
    serializer_class = EnquirySerializers
    queryset = UserEnquiry.objects.all()
    permission_classes = (IsAuthenticated,)
