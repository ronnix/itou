import json
import logging

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from itou.utils.perms.user import KIND_JOB_SEEKER, KIND_PRESCRIBER, KIND_SIAE_STAFF


logger = logging.getLogger(__name__)


class EligibilityDiagnosis(models.Model):
    """
    Store the eligibility diagnosis of a job seeker.
    """

    AUTHOR_KIND_JOB_SEEKER = KIND_JOB_SEEKER
    AUTHOR_KIND_PRESCRIBER = KIND_PRESCRIBER
    AUTHOR_KIND_SIAE_STAFF = KIND_SIAE_STAFF

    AUTHOR_KIND_CHOICES = (
        (AUTHOR_KIND_JOB_SEEKER, _("Demandeur d'emploi")),
        (AUTHOR_KIND_PRESCRIBER, _("Prescripteur")),
        (AUTHOR_KIND_SIAE_STAFF, _("Employeur (SIAE)")),
    )

    job_seeker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Demandeur d'emploi"),
        on_delete=models.CASCADE,
        related_name="eligibility_diagnoses",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Auteur"),
        on_delete=models.CASCADE,
        related_name="eligibility_diagnoses_made",
    )
    author_kind = models.CharField(
        verbose_name=_("Type de l'auteur"),
        max_length=10,
        choices=AUTHOR_KIND_CHOICES,
        default=AUTHOR_KIND_PRESCRIBER,
    )
    # When the author is an SIAE staff member, keep a track of his current SIAE.
    author_siae = models.ForeignKey(
        "siaes.Siae",
        verbose_name=_("SIAE de l'auteur"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    # When the author is a prescriber, keep a track of his current organization (if any).
    author_prescriber_organization = models.ForeignKey(
        "prescribers.PrescriberOrganization",
        verbose_name=_("Organisation du prescripteur de l'auteur"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    form_version = models.CharField(
        verbose_name=_("Version du formulaire"), max_length=10
    )
    form_cleaned_data = JSONField(verbose_name=_("Données du formulaire"))

    # Stores the diagnosis as a human readable dict structure.
    data = JSONField(verbose_name=_("Résultat du formulaire"))

    created_at = models.DateTimeField(
        verbose_name=_("Date de création"), default=timezone.now, db_index=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Date de modification"), blank=True, null=True, db_index=True
    )

    class Meta:
        verbose_name = _("Diagnostic d'éligibilité")
        verbose_name_plural = _("Diagnostics d'éligibilité")
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    @property
    def data_as_dict(self):
        if self.data:
            return json.loads(self.data)
        return {}

    @property
    def data_as_html(self):
        html = "<ul>"
        for category, choices in self.data_as_dict.items():
            html += f"<li><b>{category}</b>"
            for item in choices:
                html += "<ul>"
                html += f"<li>{item[0]}"
                html += "<ul>"
                for sub_item in item[1]:
                    html += f"<li>{sub_item}</li>"
                html += "</ul>"
                html += "</li>"
                html += "</ul>"
            html += f"</li>"
        html += "</ul>"
        return mark_safe(html)