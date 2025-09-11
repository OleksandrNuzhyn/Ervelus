from rest_framework import serializers
from .models import TermsVersion


class TermsVersionSerializer(serializers.ModelSerializer):
    document_type = serializers.CharField(source='get_document_type_display')

    class Meta:
        model = TermsVersion
        fields = ('id', 'document_type', 'version', 'content')