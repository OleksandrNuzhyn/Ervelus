from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from gdpr_assist.signals import pre_anonymise
from django.dispatch import receiver
from auditlog.models import LogEntry
from django.db.models import Q

User = get_user_model()


@receiver(pre_anonymise, sender=User)
def delete_user_log_entries(sender, instance, **kwargs):
    log_entries_to_delete = Q(actor=instance)

    objects_to_check = [
        instance,
        *instance.subscriptions.all(),
        *instance.agreements.all(),
        *instance.generation_requests.all(),
        *instance.emailaddress_set.all(),
        *instance.socialaccount_set.all()
    ]

    if hasattr(instance, 'profile'):
        objects_to_check.append(instance.profile)

    for obj in objects_to_check:
        if obj is None:
            continue
        ct = ContentType.objects.get_for_model(obj)
        log_entries_to_delete |= Q(content_type=ct, object_pk=str(obj.pk))

    LogEntry.objects.filter(log_entries_to_delete).delete()