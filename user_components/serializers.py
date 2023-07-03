from rest_framework import serializers

from user_components.models import UserEnquiry


class EnquirySerializers(serializers.ModelSerializer):
    class Meta:
        model = UserEnquiry
        fields = '__all__'
