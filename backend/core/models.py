from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from solo.models import SingletonModel
from auditlog.models import LogEntry
from django.db.models import Q
from django.db import models
import gdpr_assist


class LogEntryPrivacyMeta:
    can_anonymise = False

    def search(self, value):
        User = get_user_model()

        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            return self.model.objects.none()

        log_entries_to_export = Q(actor=user)

        objects_to_check = [
            user,
            *user.subscriptions.all(),
            *user.agreements.all(),
            *user.generation_requests.all(),
            *user.emailaddress_set.all(),
            *user.socialaccount_set.all()
        ]

        if hasattr(user, 'profile'):
            objects_to_check.append(user.profile)

        for obj in objects_to_check:
            if obj is None:
                continue
            ct = ContentType.objects.get_for_model(obj)
            log_entries_to_export |= Q(content_type=ct, object_pk=str(obj.pk))

        return self.model.objects.filter(log_entries_to_export)

    def export(self, instance):
        return {
            'object_repr': instance.object_repr,
            'action': instance.action,
            'changes': instance.changes_str,
            'timestamp': instance.timestamp,
            'remote_addr': instance.remote_addr,
            'actor_email': instance.actor.email
        }


gdpr_assist.register(LogEntry, LogEntryPrivacyMeta)


class ApplicationConfig(SingletonModel):
    is_registration_enabled = models.BooleanField(default=True)
    hard_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    reserved_for_spend = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Application Configuration"

    def __str__(self):
        return "Application Configuration"