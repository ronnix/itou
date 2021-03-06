from django.contrib import admin

from itou.job_applications import models


class TransitionLogInline(admin.TabularInline):
    model = models.JobApplicationTransitionLog
    extra = 0
    raw_id_fields = ("user",)
    can_delete = False
    readonly_fields = ("transition", "from_state", "to_state", "user", "timestamp")

    def has_add_permission(self, request):
        return False


class JobsInline(admin.TabularInline):
    model = models.JobApplication.selected_jobs.through
    extra = 1
    raw_id_fields = ("siaejobdescription",)


@admin.register(models.JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ("id", "state", "job_seeker", "sender", "sender_kind", "created_at")
    raw_id_fields = (
        "job_seeker",
        "sender",
        "sender_siae",
        "sender_prescriber_organization",
        "to_siae",
    )
    exclude = ("selected_jobs",)
    list_filter = ("sender_kind", "state", "to_siae__department")
    readonly_fields = ("created_at", "updated_at")
    inlines = (JobsInline, TransitionLogInline)
    search_fields = ("to_siae__siret",)


@admin.register(models.JobApplicationTransitionLog)
class JobApplicationTransitionLogAdmin(admin.ModelAdmin):
    actions = None
    date_hierarchy = "timestamp"
    list_display = (
        "job_application",
        "transition",
        "from_state",
        "to_state",
        "user",
        "timestamp",
    )
    list_filter = ("transition",)
    raw_id_fields = ("job_application", "user")
    readonly_fields = (
        "job_application",
        "transition",
        "from_state",
        "to_state",
        "user",
        "timestamp",
    )
    search_fields = ("transition", "user__username")
