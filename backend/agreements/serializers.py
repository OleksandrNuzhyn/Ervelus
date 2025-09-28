from rest_framework import serializers
from .models import TermsVersion


class TermsVersionSerializer(serializers.ModelSerializer):
    document_type = serializers.CharField(source='get_document_type_display')

    class Meta:
        model = TermsVersion
        fields = ('id', 'document_type', 'version', 'content')


class AcceptUserDocumentVersionSerializer(serializers.Serializer):
    terms_version_id = serializers.IntegerField()

    def validate_terms_version_id(self, value):
        if not TermsVersion.objects.filter(id=value).exists():
            raise serializers.ValidationError("Terms version with this ID does not exist")
        return value