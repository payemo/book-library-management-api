from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE books_book RENAME TO books;"
        ),
    ]
