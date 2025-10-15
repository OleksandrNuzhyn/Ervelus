from rest_framework import serializers
from subscriptions.models import UserSubscription
from .models import GenerationRequest
from urllib.parse import urlparse
from . import services
import os


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
        chosen_style = data['chosen_style']

        active_user_subscriptions = list(
            user.subscriptions.filter(
                status=UserSubscription.SubscriptionStatus.ACTIVE
            ).select_related('plan').prefetch_related('plan__unlocked_styles')
        )

        if not active_user_subscriptions:
            raise serializers.ValidationError("You don't have an active subscription")

        total_credits = sum(sub.remaining_credits for sub in active_user_subscriptions)
        if total_credits == 0:
            raise serializers.ValidationError("All credits on active subscriptions have been used")

        best_user_subscription = max(active_user_subscriptions, key=lambda sub: sub.plan.price)

        if chosen_style not in best_user_subscription.plan.unlocked_styles.all():
            raise serializers.ValidationError(f"The style '{chosen_style.name}' isn't available in your best subscription plan")

        return data


class GenerationRequestListSerializer(serializers.ModelSerializer):
    input_img_signed_url = serializers.SerializerMethodField()
    output_img_signed_url = serializers.SerializerMethodField()

    def get_img_signed_url(self, original_img_url):
        if not original_img_url:
            return None

        existing_blobs_names = self.context.get('existing_blobs_names', [])
        
        base_url, _ = os.path.splitext(original_img_url)
        thumbnail_url = f"{base_url}_200x200.webp"
        
        path = urlparse(thumbnail_url).path.lstrip('/')
        _, thumbnail_blob_name = path.split('/', 1)

        img_url_to_sign = thumbnail_url if thumbnail_blob_name in existing_blobs_names else original_img_url
        
        return services.generate_signed_gcs_url(img_url_to_sign, expires_in_seconds=300)

    def get_input_img_signed_url(self, obj):
        try:
            return self.get_img_signed_url(obj.input_img_url)
        except Exception:
            return None

    def get_output_img_signed_url(self, obj):
        try:
            return self.get_img_signed_url(obj.output_img_url)
        except Exception:
            return None

    class Meta:
        model = GenerationRequest
        fields = (
            'id',
            'status',
            'input_img_signed_url',
            'output_img_signed_url'
        )


class GenerationRequestSerializer(serializers.ModelSerializer):
    input_img_signed_url = serializers.SerializerMethodField()
    output_img_signed_url = serializers.SerializerMethodField()
    chosen_style_name = serializers.CharField(source='chosen_style.name')

    def get_input_img_signed_url(self, obj):
        try:
            if not obj.input_img_url:
                return None
            return services.generate_signed_gcs_url(obj.input_img_url, expires_in_seconds=300)
        except Exception:
            return None

    def get_output_img_signed_url(self, obj):
        try:
            if not obj.output_img_url:
                return None
            return services.generate_signed_gcs_url(obj.output_img_url, expires_in_seconds=300)
        except Exception:
            return None
        
    class Meta:
        model = GenerationRequest
        fields = (
            'id', 
            'chosen_style',
            'chosen_style_name',
            'input_img_signed_url',
            'output_img_signed_url',
            'status',
            'created_at',
            'error_message',
            'error_api_message'
        )