# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 20:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='bullet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(max_length=20, verbose_name='Producent')),
                ('bullet', models.CharField(max_length=20, verbose_name='Pocisk')),
                ('weight', models.DecimalField(decimal_places=0, max_digits=3, verbose_name='Waga [gr]')),
                ('calibration', models.CharField(max_length=5, verbose_name='Kalibracja [in]')),
                ('length', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='D\u0142ugo\u015b\u0107 [mm]')),
                ('bc', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True, verbose_name='BC')),
                ('comment', models.TextField(blank=True, default='', max_length=125, verbose_name='Komentarz')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Data')),
            ],
            options={
                'ordering': ['vendor', 'calibration', 'weight'],
            },
        ),
        migrations.CreateModel(
            name='caliber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caliber', models.CharField(max_length=20, verbose_name='Kaliber')),
                ('comment', models.TextField(blank=True, default='', max_length=125, verbose_name='Komentarz')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Data')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='W\u0142a\u015bciciel')),
            ],
            options={
                'ordering': ['caliber'],
            },
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Data')),
                ('gun', models.CharField(blank=True, default='', max_length=50, verbose_name='Bro\u0144')),
                ('comment', models.TextField(default='', max_length=140, verbose_name='Komentarz')),
            ],
        ),
        migrations.CreateModel(
            name='loads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Data')),
                ('gun', models.CharField(blank=True, default='', max_length=30, verbose_name='Bro\u0144')),
                ('COL', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='COL [mm]')),
                ('load', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Nawa\u017cka [gr]')),
                ('crimp', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Crimp [mm]')),
                ('prime', models.CharField(blank=True, default='', max_length=10, verbose_name='Sp\u0142onka')),
                ('case', models.CharField(blank=True, default='', max_length=10, verbose_name='\u0141uska')),
                ('votes', models.IntegerField(default=0, verbose_name='G\u0142osy')),
                ('bullet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reload.bullet', verbose_name='Pocisk')),
                ('caliber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reload.caliber', verbose_name='Kaliber')),
            ],
        ),
        migrations.CreateModel(
            name='powder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(max_length=20, verbose_name='Producent')),
                ('powder', models.CharField(max_length=20, verbose_name='Proch')),
                ('comment', models.TextField(blank=True, default='', max_length=125, verbose_name='Komentarz')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Data')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='W\u0142a\u015bciciel')),
            ],
            options={
                'ordering': ['vendor', 'powder'],
            },
        ),
        migrations.CreateModel(
            name='quality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quality', models.CharField(max_length=20, verbose_name='Przeznaczenie')),
            ],
            options={
                'ordering': ['quality'],
            },
        ),
        migrations.CreateModel(
            name='score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=20, verbose_name='Ocena')),
            ],
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Data')),
                ('gun', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Bro\u0144')),
                ('v0t', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True, verbose_name='V0 (QL) [m/s]')),
                ('v0c', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True, verbose_name='V0 (chrono) [m/s]')),
                ('temp', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True, verbose_name='Temp. [C]')),
                ('moa', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='Grupa [MOA]')),
                ('comment', models.TextField(blank=True, default='', max_length=125, null=True, verbose_name='Opis')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='tests/', verbose_name='Zdj\u0119cie')),
                ('load', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reload.loads', verbose_name='Elaboracja')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='W\u0142a\u015bciciel')),
            ],
        ),
        migrations.AddField(
            model_name='loads',
            name='powder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reload.powder', verbose_name='Proch'),
        ),
        migrations.AddField(
            model_name='loads',
            name='quality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reload.quality', verbose_name='Przeznaczenie'),
        ),
        migrations.AddField(
            model_name='loads',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='W\u0142a\u015bciciel'),
        ),
        migrations.AddField(
            model_name='comment',
            name='load',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reload.loads', verbose_name='Elaboracja'),
        ),
        migrations.AddField(
            model_name='comment',
            name='score',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reload.score', verbose_name='Ocena'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='W\u0142a\u015bciciel'),
        ),
        migrations.AddField(
            model_name='bullet',
            name='caliber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reload.caliber', verbose_name='Kaliber'),
        ),
        migrations.AddField(
            model_name='bullet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='W\u0142a\u015bciciel'),
        ),
    ]