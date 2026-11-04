import uuid
from django.db import migrations, models


def populate_uuids(apps, schema_editor):
    Article = apps.get_model('articles_app', 'Article')
    for article in Article.objects.filter(uuid__isnull=True).only('pk'):
        article.uuid = uuid.uuid4()
        article.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('articles_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='article',
            name='uuid',
            field=models.UUIDField(null=True, editable=False),
        ),
        migrations.RunPython(populate_uuids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='article',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
