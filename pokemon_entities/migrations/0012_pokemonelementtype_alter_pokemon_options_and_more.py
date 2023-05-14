# Generated by Django 4.2.1 on 2023-05-12 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0011_auto_20230511_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonElementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название стихии')),
            ],
            options={
                'verbose_name': 'Стихия покемона',
                'verbose_name_plural': 'Стихии покемонов',
            },
        ),
        migrations.AlterModelOptions(
            name='pokemon',
            options={'verbose_name': 'Покемон', 'verbose_name_plural': 'Покемоны'},
        ),
        migrations.AlterModelOptions(
            name='pokemonentity',
            options={'verbose_name': 'Сущность покемона', 'verbose_name_plural': 'Сущности покемонов'},
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_evolution', to='pokemon_entities.pokemon', unique=True, verbose_name='Предок'),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='element_type',
            field=models.ManyToManyField(blank=True, related_name='pokemons', to='pokemon_entities.pokemonelementtype', verbose_name='Стихии'),
        ),
    ]