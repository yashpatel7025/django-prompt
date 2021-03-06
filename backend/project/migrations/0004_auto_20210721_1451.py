# Generated by Django 3.1.5 on 2021-07-21 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_install_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackrequest',
            name='picked_up_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='picked_up_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('feedback_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='project.feedbackrequest')),
            ],
        ),
    ]
