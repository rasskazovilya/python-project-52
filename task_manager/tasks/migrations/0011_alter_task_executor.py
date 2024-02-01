# Generated by Django 3.2.23 on 2024-02-01 07:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0010_auto_20240126_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='performer_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Performer'),
        ),
    ]