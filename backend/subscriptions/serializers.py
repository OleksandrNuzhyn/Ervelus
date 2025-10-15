from rest_framework import serializers
from .models import UserSubscription


class UserSubscriptionListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='display_status')
    plan_name = serializers.CharField(source='plan.name')
    plan_description = serializers.CharField(source='plan.description')
    plan_price = serializers.DecimalField(source='plan.price', max_digits=8, decimal_places=2)
    plan_generations_count = serializers.IntegerField(source='plan.generations_count')
    plan_unlocked_styles_count = serializers.IntegerField()

    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'plan_name',
            'plan_description',
            'plan_price',
            'plan_generations_count',
            'plan_unlocked_styles_count',
            'start_time', 
            'end_time', 
            'status', 
            'remaining_credits'
        ]


class SubscriptionEligibilityCheckSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()