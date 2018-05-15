# Generated by Django 2.0.1 on 2018-05-14 20:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analisys_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('json_result', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, max_length=50, null=True)),
                ('query', models.CharField(blank=True, max_length=200, null=True)),
                ('number_of_messages', models.IntegerField(blank=True, null=True)),
                ('saved', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('finish_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Twitter_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=500)),
                ('likes', models.IntegerField()),
                ('retweets', models.IntegerField()),
                ('replies', models.IntegerField()),
                ('dataset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('screen_name', models.CharField(default='username', max_length=200)),
                ('name', models.CharField(blank=True, default='name', max_length=200, null=True)),
                ('statuses_count', models.IntegerField()),
                ('following', models.IntegerField()),
                ('followers', models.IntegerField()),
                ('likes', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='twitter_data',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.User'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='project',
            field=models.ForeignKey(on_delete='models.CASCADE', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='analisys_data',
            name='dataset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Dataset'),
        ),
        migrations.AddField(
            model_name='analisys_data',
            name='project',
            field=models.ForeignKey(on_delete='models.CASCADE', to='projects.Project'),
        ),
    ]
