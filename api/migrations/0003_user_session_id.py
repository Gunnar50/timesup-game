# Generated by Django 4.2.3 on 2023-07-20 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_room_user_delete_waitingroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='session_id',
            field=models.CharField(default='test', max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
