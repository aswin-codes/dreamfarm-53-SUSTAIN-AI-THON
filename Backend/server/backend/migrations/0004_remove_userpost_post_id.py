# Generated by Django 4.2.7 on 2024-03-02 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_remove_comments_post_id_remove_market_prod_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpost',
            name='post_id',
        ),
    ]
