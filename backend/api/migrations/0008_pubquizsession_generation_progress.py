# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_pubquizsession_session_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='pubquizsession',
            name='generation_progress',
            field=models.JSONField(blank=True, help_text='Progress data for question generation: {progress: int, status: str}', null=True),
        ),
    ]
