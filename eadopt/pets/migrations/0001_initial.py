# Generated by Django 2.0.3 on 2018-06-22 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('binario', models.BinaryField()),
                ('formato', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=80)),
                ('especie', models.CharField(max_length=80)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('id_mongo', models.CharField(blank=True, max_length=24, null=True)),
                ('dono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Usuario')),
            ],
        ),
        migrations.AddField(
            model_name='foto',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.Pet'),
        ),
    ]