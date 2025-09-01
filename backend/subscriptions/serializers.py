from rest_framework import serializers
from .models import UserSubscription


class UserSubscriptionListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='display_status')
    plan_name = serializers.CharField(source='plan.name')

    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'plan_name',
            'start_time', 
            'end_time', 
            'status', 
            'remaining_credits'
        ]


class SubscriptionEligibilityCheckSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()