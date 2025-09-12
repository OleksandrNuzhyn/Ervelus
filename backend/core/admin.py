from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import ApplicationConfig
from auditlog.models import LogEntry
from auditlog.admin import LogEntryAdmin

OriginalLogEntryAdmin = LogEntryAdmin
admin.site.unregister(LogEntry)

LogEntry._meta.verbose_name = "Audit Record"
LogEntry._meta.verbose_name_plural = "Audit Records"

@admin.register(LogEntry)
class CustomLogEntryAdmin(OriginalLogEntryAdmin):
    readonly_fields = (
        'id',
        'object_pk',
        'object_repr',
        'action',
        'changes',
        'timestamp',
        'actor',
        'content_type',
        'remote_addr'
    )
    
    fieldsets = (
        (None, {
            'fields': ('timestamp', 'actor', 'remote_addr')
        }),
        ('Resource', {
            'fields': ('object_pk', 'object_repr', 'content_type')
        }),
        ('Changes', {
            'fields': ('action', 'changes')
        })
    )


@admin.register(ApplicationConfig)
class ApplicationConfigAdmin(SingletonModelAdmin):
    readonly_fields = ('reserved_for_spend',)