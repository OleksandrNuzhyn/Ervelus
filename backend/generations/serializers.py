from adrf import serializers
from subscriptions.models import UserSubscription
from .models import GenerationRequest


class GenerationRequestCreateSerializer(serializers.ModelSerializer):
    RESOLUTION_CHOICES = [
        ('1536x1024', '1536x1024'),
        ('1024x1536', '1024x1536'),
        ('1024x1024', '1024x1024'),
    ]
    input_image = serializers.ImageField(write_only=True, required=True)
    resolution = serializers.ChoiceField(choices=RESOLUTION_CHOICES, write_only=True, required=True)

    class Meta:
        model = GenerationRequest
        fields = ('input_image', 'resolution', 'chosen_style')

    async def validate_input_image(self, value):
        allowed_content_types = ['image/jpeg', 'image/png', 'image/webp']
        if value.content_type not in allowed_content_types:
            raise serializers.ValidationError("Invalid image format. Allowed formats are: JPG, PNG, WebP")
        
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(f"Image size cannot exceed 10 MB. Your file is {value.size // 1024 // 1024} MB")
        
        return value

    async def validate(self, data):
        user = self.context['request'].user
        chosen_style = data['chosen_style']

        active_user_subscriptions = [
            sub async for sub in user.subscriptions.filter(
                status=UserSubscription.SubscriptionStatus.ACTIVE
            ).select_related('plan').prefetch_related('plan__unlocked_styles')
        ]

        if not active_user_subscriptions:
            raise serializers.ValidationError("You don't have an active subscription")

        total_credits = sum(sub.generations_count for sub in active_user_subscriptions)
        if total_credits == 0:
            raise serializers.ValidationError("All credits on active subscriptions have been used")

        best_user_subscription = max(active_user_subscriptions, key=lambda sub: sub.plan.price)

        if chosen_style not in best_user_subscription.plan.unlocked_styles.all():
            raise serializers.ValidationError(f"The style '{chosen_style.name}' isn't available in your best subscription plan")

        return data


class GenerationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerationRequest
        fields = (
            'id', 
            'chosen_style',
            'input_img_url',
            'output_img_url',
            'status',
            'error_message',
            'error_api_message',
            'created_at',
            'updated_at'
        )