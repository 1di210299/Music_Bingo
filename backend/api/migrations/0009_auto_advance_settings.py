# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_pubquizsession_generation_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='pubquizsession',
            name='auto_advance_enabled',
            field=models.BooleanField(default=False, help_text='Auto-advance to next question'),
        ),
        migrations.AddField(
            model_name='pubquizsession',
            name='auto_advance_seconds',
            field=models.IntegerField(default=15, help_text='Seconds before auto-advancing'),
        ),
        migrations.AddField(
            model_name='pubquizsession',
            name='auto_advance_paused',
            field=models.BooleanField(default=False, help_text='Timer is paused'),
        ),
        migrations.AddField(
            model_name='pubquizsession',
            name='question_started_at',
            field=models.DateTimeField(blank=True, help_text='When current question started', null=True),
        ),
    ]
