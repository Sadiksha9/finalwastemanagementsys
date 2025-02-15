# Generated by Django 5.1.5 on 2025-01-25 11:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WasteImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='waste_images/')),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('classification_result', models.CharField(choices=[('organic', 'Organic'), ('recyclable', 'Recyclable'), ('hazardous', 'Hazardous'), ('other', 'Other'), ('unclassified', 'Unclassified')], default='unclassified', max_length=20)),
                ('confidence_score', models.FloatField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
