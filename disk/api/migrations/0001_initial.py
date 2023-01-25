# Generated by Django 4.1.5 on 2023-01-25 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=255, null=True)),
                ('type', models.CharField(choices=[('FOLDER', 'FOLDER'), ('FILE', 'FILE')], max_length=6)),
                ('date', models.DateTimeField()),
                ('size', models.IntegerField()),
                ('parentId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='api.content')),
            ],
        ),
    ]