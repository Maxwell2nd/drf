# Generated by Django 2.2.1 on 2019-05-19 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_auto_20190328_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.CharField(choices=[('L', 'Like'), ('D', 'Dislike')], default='L', max_length=1)),
                ('voted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voted_by', to='social.Post')),
                ('voted_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voted_post', to='social.Post')),
            ],
        ),
        migrations.RemoveField(
            model_name='likes',
            name='liked_by',
        ),
        migrations.RemoveField(
            model_name='likes',
            name='liked_post',
        ),
        migrations.DeleteModel(
            name='Dislikes',
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
    ]
