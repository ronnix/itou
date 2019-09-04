# Generated by Django 2.2.4 on 2019-09-04 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("siaes", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("jobs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="siaemembership",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="siaejobs",
            name="appellation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="jobs.Appellation"
            ),
        ),
        migrations.AddField(
            model_name="siaejobs",
            name="siae",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="jobs_through",
                to="siaes.Siae",
            ),
        ),
        migrations.AddField(
            model_name="siae",
            name="jobs",
            field=models.ManyToManyField(
                blank=True,
                through="siaes.SiaeJobs",
                to="jobs.Appellation",
                verbose_name="Métiers",
            ),
        ),
        migrations.AddField(
            model_name="siae",
            name="members",
            field=models.ManyToManyField(
                blank=True,
                through="siaes.SiaeMembership",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Membres",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="siaejobs", unique_together={("appellation", "siae")}
        ),
    ]