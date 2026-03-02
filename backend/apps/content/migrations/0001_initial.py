from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('summary', models.TextField()),
                ('content', models.TextField()),
                ('cover_image', models.URLField(blank=True)),
                ('youtube_url', models.URLField(blank=True)),
                ('youtube_video_id', models.CharField(blank=True, max_length=11)),
                ('show_in_gallery', models.BooleanField(default=False)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={'ordering': ['-published_at', '-created_at']},
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('cover_image', models.URLField(blank=True)),
                ('youtube_url', models.URLField(blank=True)),
                ('youtube_video_id', models.CharField(blank=True, max_length=11)),
                ('show_in_gallery', models.BooleanField(default=False)),
            ],
            options={'ordering': ['start_date']},
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=160)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='uploads/%Y/%m/')),
                ('type', models.CharField(choices=[('image', 'Imagem'), ('video', 'Vídeo')], max_length=10)),
                ('public_url', models.URLField(blank=True)),
                ('related_article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.article')),
                ('related_event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.event')),
            ],
            options={'verbose_name_plural': 'media'},
        ),
    ]
