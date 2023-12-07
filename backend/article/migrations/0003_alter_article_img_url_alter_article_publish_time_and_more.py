# Generated by Django 4.2.1 on 2023-08-20 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_article_comment_delete_articlepost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='img_url',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='图片路径'),
        ),
        migrations.AlterField(
            model_name='article',
            name='publish_time',
            field=models.IntegerField(default=1692521460, verbose_name='发布时间'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_time',
            field=models.IntegerField(default=1692521460, verbose_name='评论时间'),
        ),
    ]
