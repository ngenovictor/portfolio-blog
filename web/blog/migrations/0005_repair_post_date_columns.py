from django.db import migrations

# 0001 used to create date_created/date_updated as TimeField and 0004 altered
# them to DateTimeField, which Postgres can't do (no time -> timestamptz cast).
# 0001 was later changed to create DateTimeField directly, making 0004 a no-op,
# but a database that ran the old 0001 and then the no-op 0004 still has `time`
# columns, so posts have no date. Convert any such columns in place. A time of
# day carries no date, so existing rows get the date the migration runs.
# Databases with correct columns, and non-Postgres databases, are untouched.

COLUMNS = ("date_created", "date_updated")


def repair_date_columns(apps, schema_editor):
    connection = schema_editor.connection
    if connection.vendor != "postgresql":
        return
    table = apps.get_model("blog", "Post")._meta.db_table
    with connection.cursor() as cursor:
        for column in COLUMNS:
            cursor.execute(
                "SELECT data_type FROM information_schema.columns "
                "WHERE table_schema = current_schema() AND table_name = %s AND column_name = %s",
                [table, column],
            )
            row = cursor.fetchone()
            if row and row[0] == "time without time zone":
                quoted_table = schema_editor.quote_name(table)
                quoted_column = schema_editor.quote_name(column)
                schema_editor.execute(
                    f"ALTER TABLE {quoted_table} ALTER COLUMN {quoted_column} "
                    f"TYPE timestamp with time zone "
                    f"USING (CURRENT_DATE + {quoted_column}) AT TIME ZONE 'UTC'"
                )


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_post_date_created_alter_post_date_updated"),
    ]

    operations = [
        migrations.RunPython(repair_date_columns, migrations.RunPython.noop),
    ]
