from rest_framework import serializers
from .models import TermsVersion


class TermsVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsVersion
        fields = ['document_type', 'version', 'content', 'published_at']