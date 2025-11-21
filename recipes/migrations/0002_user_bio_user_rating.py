import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(limit_value=0.0, message='Rating must be greater than or equal to 0.0'), django.core.validators.MaxValueValidator(limit_value=5.0, message='Rating must be less than or equal to 5.0')]),
        ),
    ]