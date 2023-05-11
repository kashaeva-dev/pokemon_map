import datetime

from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Название по-русски")
    title_en = models.CharField(max_length=200, verbose_name="Название по-английски")
    title_jp = models.CharField(max_length=200, verbose_name="Название по-японски")
    photo = models.ImageField(upload_to='pokemons', null=True, blank=True, verbose_name="Изображение")
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Предок', null=True, blank=True, unique=True)

    def __str__(self):
        return str(self.title_ru)

    def next_evolution(self):
        try:
            next_evolution = self.__class__.objects.get(parent=self)
        except self.DoesNotExist:
            next_evolution = False

        return next_evolution


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон", related_name="entities")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(verbose_name='Здоровье')
    strength = models.IntegerField(verbose_name='Сила')
    defence = models.IntegerField(verbose_name='Защита')
    stamina = models.IntegerField(verbose_name='Выносливость')
