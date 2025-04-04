# Generated by Django 5.1.7 on 2025-04-02 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0004_tree_progenitor_alter_tree_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tree',
            name='progenitor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tree_progenitor', to='trees.person', verbose_name='Родоначальник'),
        ),
    ]
