# Generated manually for soft-delete support on Article

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles_app', '0002_alter_article_options_article_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
