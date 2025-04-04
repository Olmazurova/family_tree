# Generated by Django 5.1.7 on 2025-04-03 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0006_remove_person_child_person_child'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tree',
            name='progenitor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tree_progenitor', to='trees.person', verbose_name='Родоначальник'),
        ),
    ]
