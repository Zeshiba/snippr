# Generated by Django 2.1.1 on 2018-10-24 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snippr', '0010_auto_20181023_0508'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=500)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameField(
            model_name='commit',
            old_name='lastest_update',
            new_name='latest_update',
        ),
        migrations.RemoveField(
            model_name='commit',
            name='code',
        ),
        migrations.AddField(
            model_name='snippet',
            name='commit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to='snippr.Commit'),
        ),
        migrations.AddField(
            model_name='snippet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL),
        ),
    ]