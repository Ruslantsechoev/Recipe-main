# Generated by Django 4.2.7 on 2025-02-04 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_category_recipe_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='image',
        ),
        migrations.AddField(
            model_name='recipe',
            name='image_base64',
            field=models.TextField(blank=True, null=True, verbose_name='Изображение (Base64)'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]
