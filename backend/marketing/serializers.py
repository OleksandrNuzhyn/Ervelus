from rest_framework import serializers


class ApplyPromoCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)

    def validate_code(self, value):
        return value.strip()