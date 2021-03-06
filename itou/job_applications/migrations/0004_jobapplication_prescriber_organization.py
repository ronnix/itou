# Generated by Django 2.2.6 on 2019-10-16 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("prescribers", "0006_auto_20191015_1152"),
        ("job_applications", "0003_remove_jobapplication_prescriber_organization"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplication",
            name="prescriber_organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="prescribers.PrescriberOrganization",
                verbose_name="Organisation du prescripteur",
            ),
        )
    ]
