# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=300)),
                ('passwd', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Partida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_partida', models.IntegerField()),
                ('estat', models.CharField(default=b'INACTIVA', max_length=20)),
                ('classe', models.CharField(max_length=100, null=True)),
                ('usuaris_registrats', models.IntegerField(default=0)),
                ('data_creacio', models.DateTimeField()),
                ('data_inicialitzacio', models.DateTimeField(null=True)),
                ('data_finalitzacio', models.DateTimeField(null=True)),
                ('comentari', models.CharField(max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_id', models.IntegerField(default=0)),
                ('nickname', models.CharField(default=b'', max_length=100)),
                ('name', models.CharField(default=b'', max_length=100)),
                ('selection', models.CharField(default=b'', max_length=1)),
                ('last_selected', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(default=b'', max_length=100)),
                ('on_vius', models.CharField(default=b'', max_length=6)),
                ('genere', models.CharField(default=b'', max_length=1)),
                ('rang_edat', models.CharField(default=b'', max_length=100)),
                ('check1', models.BooleanField(default=False)),
                ('num_jugador', models.IntegerField(null=True)),
                ('status', models.CharField(default=b'', max_length=100)),
                ('session_game', models.CharField(default=b'', max_length=100)),
                ('game1', models.ForeignKey(related_name='standard', to='game.Partida', null=True)),
                ('game2', models.ForeignKey(related_name='interact', to='game.Partida', null=True)),
                ('game3', models.ForeignKey(related_name='voive', to='game.Partida', null=True)),
                ('game4', models.ForeignKey(related_name='wall', to='game.Partida', null=True)),
                ('partida_current', models.ForeignKey(related_name='current', to='game.Partida', null=True)),                ('money_game1', models.FloatField(default=0)),
                ('money_game2', models.FloatField(default=0)),
                ('money_game4', models.FloatField(default=0)),
                ('money_game3', models.FloatField(default=0)),
                ('punts_totals', models.FloatField(default=0)),
                ('guany_final', models.IntegerField(default=0)),
                ('is_robot', models.BooleanField(default=False)),
                ('num_seleccions', models.IntegerField(default=0)),
                ('acabat', models.BooleanField(default=False)),
                ('data_creacio', models.DateTimeField()),
                ('date_register_game1', models.DateTimeField(null=True)),
                ('date_register_game2', models.DateTimeField(null=True)),
                ('date_register_game3', models.DateTimeField(null=True)),
                ('date_register_game4', models.DateTimeField(null=True)),
                ('date_end_game1', models.DateTimeField(null=True)),
                ('date_end_game2', models.DateTimeField(null=True)),
                ('date_end_game3', models.DateTimeField(null=True)),
                ('date_end_game4', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prisoner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_robot1', models.BooleanField(default=True)),
                ('rol1', models.CharField(default=b'', max_length=100)),
                ('user', models.ForeignKey(to='game.User')),
                ('rival1',models.ForeignKey(related_name='rival_prisoner1', blank=True, to='game.User', null=True)),
                ('rival1_resident', models.ForeignKey(related_name='rival_resident1', blank=True, to='game.Resident', null=True)),
                ('guess1', models.CharField(default=b'', max_length=1)),
                ('seleccio1', models.CharField(default=b'', max_length=1)),
                ('partida', models.ForeignKey(to='game.Partida', null=True)),
                ('gain1', models.FloatField(default=0)),
                ('data_guess1', models.DateTimeField(null=True)),
                ('data_seleccio1', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
