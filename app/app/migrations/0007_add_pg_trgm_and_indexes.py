# app/app/migrations/0007_add_pg_trgm_and_indexes.py
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_scamrecord_description_and_more'),  # adjust to latest dependency in your project
    ]

    operations = [
        # enable pg_trgm extension
        migrations.RunSQL(
            sql="CREATE EXTENSION IF NOT EXISTS pg_trgm;",
            reverse_sql="DROP EXTENSION IF EXISTS pg_trgm;",
        ),
        # create trigram GIN index on first_name and last_name
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS app_contact_first_name_trgm
            ON app_contact
            USING gin (first_name gin_trgm_ops);
            """,
            reverse_sql="DROP INDEX IF EXISTS app_contact_first_name_trgm;",
        ),
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS app_contact_last_name_trgm
            ON app_contact
            USING gin (last_name gin_trgm_ops);
            """,
            reverse_sql="DROP INDEX IF EXISTS app_contact_last_name_trgm;",
        ),
        # index on phone_number for fast exact/endswith matches
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS app_contact_phone_idx
            ON app_contact (phone_number);
            """,
            reverse_sql="DROP INDEX IF EXISTS app_contact_phone_idx;",
        ),
    ]
