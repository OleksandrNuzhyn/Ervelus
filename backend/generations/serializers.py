from core.models import ApplicationAnalytics
from rest_framework import serializers
from .models import GenerationRequest
from . import services


class GenerationRequestCreateSerializer(serializers.ModelSerializer):
    input_image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = GenerationRequest
        fields = ('input_image', 'chosen_style')

    def validate_input_image(self, value):
        allowed_content_types = ['image/jpeg', 'image/png', 'image/webp']
        if value.content_type not in allowed_content_types:
            raise serializers.ValidationError("Invalid image format. Allowed formats are: JPG, PNG, WebP")
        
        max_size = 7 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(f"Image size cannot exceed 7 MB. Your file is {value.size // 1024 // 1024} MB")
        
        return value

    def validate(self, data):
        user = self.context['request'].user
        profile = user.profile
        
        if profile.free_credits > 0:
            if profile.is_paid or ApplicationAnalytics.get_solo().is_free_generations_enabled:
                data['type'] = GenerationRequest.CreditType.FREE
                return data
            
        if profile.paid_credits > 0:
            data['type'] = GenerationRequest.CreditType.PAID
            return data
            
        if profile.free_credits > 0:
            raise serializers.ValidationError("Free usage is currently disabled")
            
        raise serializers.ValidationError("You don't have enough generations")


class GenerationRequestListSerializer(serializers.ModelSerializer):
    input_thumb_signed_url = serializers.SerializerMethodField()
    output_thumb_signed_url = serializers.SerializerMethodField()

    def get_input_thumb_signed_url(self, obj):
        try:
            if not obj.input_thumb_url:
                return None
            return services.generate_signed_gcs_url(obj.input_thumb_url, expires_in_seconds=300)
        except Exception:
            return None

    def get_output_thumb_signed_url(self, obj):
        try:
            if not obj.output_thumb_url:
                return None
            return services.generate_signed_gcs_url(obj.output_thumb_url, expires_in_seconds=300)
        except Exception:
            return None

    class Meta:
        model = GenerationRequest
        fields = (
            'id',
            'input_thumb_signed_url',
            'output_thumb_signed_url'
        )


class GenerationRequestSerializer(serializers.ModelSerializer):
    input_large_signed_url = serializers.SerializerMethodField()
    output_large_signed_url = serializers.SerializerMethodField()
    chosen_style_name = serializers.CharField(source='chosen_style.name', read_only=True)

    def get_input_large_signed_url(self, obj):
        view = self.context.get('view')
        if view and view.action == 'latest':
            return None
            
        try:
            if not obj.input_large_url:
                return None
            return services.generate_signed_gcs_url(obj.input_large_url, expires_in_seconds=300)
        except Exception:
            return None

    def get_output_large_signed_url(self, obj):
        try:
            if not obj.output_large_url:
                return None
            return services.generate_signed_gcs_url(obj.output_large_url, expires_in_seconds=300)
        except Exception:
            return None
        
    class Meta:
        model = GenerationRequest
        fields = (
            'id', 
            'chosen_style',
            'chosen_style_name',
            'input_large_signed_url',
            'output_large_signed_url',
            'status',
            'created_at'
        )