# Generated by Django 2.2.6 on 2019-10-06 22:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('alumnas', models.ManyToManyField(blank=True, related_name='alumnas', to=settings.AUTH_USER_MODEL)),
                ('profesoras', models.ManyToManyField(blank=True, related_name='profesoras', to=settings.AUTH_USER_MODEL)),
                ('tema', models.ManyToManyField(blank=True, related_name='tags', to='cursos.Tema')),
                ('voluntarias', models.ManyToManyField(blank=True, related_name='voluntarias', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
