# Generated by Django 3.2.6 on 2021-08-13 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('type', models.CharField(choices=[('text', 'Text'), ('radio', 'One option'), ('checkbox', 'Multiple options')], max_length=30)),
                ('poll', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='poll_app.poll')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.TextField(verbose_name='Possible answer option')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll_app.question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.TextField(null=True)),
                ('multiple_answer', models.ManyToManyField(to='poll_app.AnswerOption')),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll_app.question')),
                ('single_answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers_single_answer', to='poll_app.answeroption')),
            ],
        ),
    ]
