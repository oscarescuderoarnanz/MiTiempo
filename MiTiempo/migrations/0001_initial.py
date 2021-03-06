# Generated by Django 2.1.7 on 2019-05-06 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autor', models.CharField(max_length=50)),
                ('texto', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_municipio', models.CharField(max_length=200)),
                ('municipio_id', models.CharField(max_length=200)),
                ('altitud', models.CharField(max_length=200)),
                ('latitud', models.CharField(max_length=200)),
                ('longitud', models.CharField(max_length=200)),
                ('precipitaion', models.CharField(max_length=200)),
                ('descripcion', models.CharField(max_length=200)),
                ('tmax', models.CharField(max_length=200)),
                ('tmin', models.CharField(max_length=200)),
                ('enlace', models.URLField(blank=True, max_length=500, null=True)),
                ('numcom', models.PositiveSmallIntegerField(default=0)),
                ('seleccionado', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='ejemplo', max_length=100)),
                ('password', models.CharField(default='ejemplo', max_length=50)),
                ('email', models.EmailField(default='example@example.com', max_length=100)),
                ('colorletras', models.PositiveSmallIntegerField(default=1)),
                ('tamanoletras', models.PositiveSmallIntegerField(default=1)),
                ('colorfondo', models.PositiveSmallIntegerField(default=1)),
                ('titulo', models.CharField(default='Página de usuario', max_length=300)),
                ('count', models.PositiveSmallIntegerField(default=0)),
                ('comentario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MiTiempo.Comentario')),
                ('municipios', models.ManyToManyField(to='MiTiempo.Municipio')),
            ],
        ),
        migrations.AddField(
            model_name='comentario',
            name='municipio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MiTiempo.Municipio'),
        ),
    ]
