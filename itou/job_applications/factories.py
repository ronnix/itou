import datetime

import factory
import factory.fuzzy

from itou.job_applications import models
from itou.prescribers.factories import (
    AuthorizedPrescriberOrganizationWithMembershipFactory,
    PrescriberOrganizationWithMembershipFactory,
)

from itou.siaes.factories import SiaeWithMembershipFactory
from itou.siaes.models import SiaeJobDescription
from itou.users.factories import PrescriberFactory, JobSeekerFactory


class JobApplicationFactory(factory.django.DjangoModelFactory):
    """Generates a JobApplication() object."""

    class Meta:
        model = models.JobApplication

    job_seeker = factory.SubFactory(JobSeekerFactory)
    to_siae = factory.SubFactory(SiaeWithMembershipFactory)
    message = factory.Faker("sentence", nb_words=40)
    answer = factory.Faker("sentence", nb_words=40)
    date_of_hiring = datetime.date.today()

    @factory.post_generation
    def selected_jobs(self, create, extracted, **kwargs):
        """
        Add selected_jobs in which the job seeker is interested.
        https://factoryboy.readthedocs.io/en/latest/recipes.html#simple-many-to-many-relationship

        Usage:
            appellation1 = Appellation.objects.filter(code='10933')
            appellation2 = Appellation.objects.filter(code='10934')
            JobApplicationFactory(selected_jobs=(appellation1, appellation2))
        """
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of jobs were passed in, use them.
            for appellation in extracted:
                siae_job_description = SiaeJobDescription.objects.create(
                    siae=self.to_siae, appellation=appellation
                )
                self.selected_jobs.add(siae_job_description)


class JobApplicationSentByJobSeekerFactory(JobApplicationFactory):
    """Generates a JobApplication() object sent by a job seeker."""

    sender = factory.SelfAttribute("job_seeker")
    sender_kind = models.JobApplication.SENDER_KIND_JOB_SEEKER


class JobApplicationSentByPrescriberFactory(JobApplicationFactory):
    """Generates a JobApplication() object sent by a prescriber."""

    sender = factory.SubFactory(PrescriberFactory)
    sender_kind = models.JobApplication.SENDER_KIND_PRESCRIBER


class JobApplicationSentByPrescriberOrganizationFactory(JobApplicationFactory):
    """Generates a JobApplication() object sent by a prescriber member of an organization."""

    sender_kind = models.JobApplication.SENDER_KIND_PRESCRIBER
    sender_prescriber_organization = factory.SubFactory(
        PrescriberOrganizationWithMembershipFactory
    )

    @factory.post_generation
    def set_sender(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        self.sender = self.sender_prescriber_organization.members.first()
        self.save()


class JobApplicationSentByAuthorizedPrescriberOrganizationFactory(
    JobApplicationFactory
):
    """Generates a JobApplication() object sent by a prescriber member of an authorized organization."""

    sender_kind = models.JobApplication.SENDER_KIND_PRESCRIBER
    sender_prescriber_organization = factory.SubFactory(
        AuthorizedPrescriberOrganizationWithMembershipFactory
    )

    @factory.post_generation
    def set_sender(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        self.sender = self.sender_prescriber_organization.members.first()
        self.save()
