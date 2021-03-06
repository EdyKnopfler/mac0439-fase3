# Generated by Django 2.0.3 on 2018-06-30 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
        ('anuncios_doacao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessoDoacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicio', models.DateField()),
                ('data_termino', models.DateField()),
                ('anuncio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anuncios_doacao.AnuncioDoacao')),
                ('candidato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Usuario')),
            ],
            options={
                'db_table': 'processo_doacao',
            },
        ),
        migrations.CreateModel(
            name='StatusRequisito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=80)),
                ('status', models.CharField(default='a verificar', max_length=12)),
                ('anuncio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anuncios_doacao.AnuncioDoacao')),
                ('candidato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Usuario')),
            ],
            options={
                'db_table': 'status_requisito',
            },
        ),
        migrations.AlterUniqueTogether(
            name='statusrequisito',
            unique_together={('anuncio', 'candidato', 'titulo')},
        ),
        migrations.AlterUniqueTogether(
            name='processodoacao',
            unique_together={('anuncio', 'candidato')},
        ),
    ]
