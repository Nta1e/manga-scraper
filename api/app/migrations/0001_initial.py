# Generated by Django 2.2.6 on 2019-10-17 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('number', models.IntegerField()),
                ('image', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.URLField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.IntegerField()),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Chapters')),
            ],
        ),
        migrations.AddField(
            model_name='chapters',
            name='manga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Manga'),
        ),
    ]
