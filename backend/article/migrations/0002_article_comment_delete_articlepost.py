# Generated by Django 4.2.1 on 2023-08-20 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='文章标题')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('publish_time', models.IntegerField(default=1692520014, verbose_name='发布时间')),
                ('img_url', models.CharField(blank=True, max_length=100, verbose_name='图片路径')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'db_table': 'article_tb',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(verbose_name='评论内容')),
                ('comment_time', models.IntegerField(default=1692520014, verbose_name='评论时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article', verbose_name='评论文章')),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='评论者')),
                ('pre_comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.comment', verbose_name='父评论id')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
                'db_table': 'comment_tb',
            },
        ),
        migrations.DeleteModel(
            name='ArticlePost',
        ),
    ]
