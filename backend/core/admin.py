from django.contrib.contenttypes.models import ContentType
from gdpr_assist.admin import PersonalData, PersonalDataAdmin
from gdpr_assist.admin.tool import PersonalDataSearchForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect, render
from gdpr_assist.registry import registry
from django.contrib import admin, messages
from solo.admin import SingletonModelAdmin
from collections import defaultdict
from .models import Application
from django import forms

admin.site.unregister(PersonalData)


class CustomPersonalDataSearchForm(PersonalDataSearchForm):
    action = forms.ChoiceField(
        label="Action",
        choices=[(PersonalDataSearchForm.ACTION_EXPORT, "Export")],
        required=False
    )


@admin.register(PersonalData)
class CustomPersonalDataAdmin(PersonalDataAdmin):
    @method_decorator(csrf_protect)
    def changelist_view(self, request, extra_context=None):
        results = None

        if request.method == "POST":
            form = CustomPersonalDataSearchForm(request.POST)
            
            if form.is_valid():
                term = form.cleaned_data["term"]
                action = form.cleaned_data["action"]
                if action:
                    raw_objs = request.POST.getlist("obj_pk")
                    group_pks = defaultdict(list)
                    for raw_obj in raw_objs:
                        content_type_id, obj_pk = raw_obj.split("-", 1)
                        group_pks[content_type_id].append(obj_pk)

                    querysets = {}
                    for content_type_id, pks in group_pks.items():
                        content_type = ContentType.objects.get_for_id(content_type_id)
                        model = content_type.model_class()
                        qs = model.anonymisable_manager().filter(pk__in=pks)
                        if qs.exists():
                            querysets[model] = qs

                    if not querysets:
                        messages.error(request, "No objects selected")
                    elif action == PersonalDataSearchForm.ACTION_EXPORT:
                        return self.handle_export(request, querysets)

                return redirect(f"{request.path}?term={term}")
        else:
            term = request.GET.get("term", "")
            form = CustomPersonalDataSearchForm(initial={"term": term})
            
            if term:
                raw_results = registry.search(term)

                results = (
                    {
                        "model": model,
                        "results": model_results,
                        "app_label": model._meta.app_label,
                        "model_name": model._meta.verbose_name,
                        "content_type": ContentType.objects.get_for_model(model),
                        "url_name": "admin:{}_{}_change".format(
                            model._meta.app_label, model._meta.model_name
                        ),
                        "url_change_name": "admin:{}_{}_changelist".format(
                            model._meta.app_label, model._meta.model_name
                        ),
                    }
                    for model, model_results in raw_results
                    if model_results
                )

        return render(
            request,
            self.change_list_template,
            {
                **self.admin_site.each_context(request),
                "title": "Personal Data",
                "form": form,
                "results": results,
                "media": self.media,
            }
        )


@admin.register(Application)
class ApplicationAdmin(SingletonModelAdmin):
    readonly_fields = (
        'users_count', 
        'users_invites',
        'users_organic_growth',
        'users_geo_count', 
        'paid_users_count',
        'sales_conversion_rate',
        'sales_geo_count',
        'sales_geo_stars'
    )
    
    fieldsets = (
        ('Users', {
            'fields': ('users_count', 'users_invites', 'users_organic_growth', 'users_geo_count')
        }),
        ('Sales', {
            'fields': ('paid_users_count', 'sales_conversion_rate', 'sales_geo_count', 'sales_geo_stars')
        }),
        ('Control', {
            'fields': ('is_free_generations_enabled',)
        })
    )