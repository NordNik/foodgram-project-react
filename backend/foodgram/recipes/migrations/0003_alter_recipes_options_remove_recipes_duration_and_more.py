# Generated by Django 4.0 on 2023-02-20 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipes',
            options={'ordering': ['-cooking_time'], 'verbose_name_plural': 'Recipes'},
        ),
        migrations.RemoveField(
            model_name='recipes',
            name='duration',
        ),
        migrations.AddField(
            model_name='recipes',
            name='cooking_time',
            field=models.IntegerField(default=0, verbose_name='Duration'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredientrecipes',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5),
        ),
    ]
