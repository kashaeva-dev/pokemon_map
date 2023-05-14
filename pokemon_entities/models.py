from django.db import models
from django.urls import reverse


class PokemonElementType(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название стихии")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Стихия покемона'
        verbose_name_plural = 'Стихии покемонов'


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Название по-русски")
    title_en = models.CharField(max_length=200, verbose_name="Название по-английски", blank=True)
    title_jp = models.CharField(max_length=200, verbose_name="Название по-японски", blank=True)
    photo = models.ImageField(upload_to='pokemons', null=True, blank=True, verbose_name="Изображение")
    description = models.TextField(verbose_name='Описание', blank=True)
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='Предок',
        null=True,
        blank=True,
        related_name='next_evolutions',
    )
    element_type = models.ManyToManyField(
        PokemonElementType,
        verbose_name='Стихии',
        blank=True,
        related_name='pokemons',
    )

    class Meta:
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'

    def __str__(self):
        return self.title_ru

    def get_absolute_url(self):
        return reverse('pokemon', args=[str(self.id)])


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон", related_name="entities")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
    strength = models.IntegerField(verbose_name='Сила', null=True, blank=True)
    defence = models.IntegerField(verbose_name='Защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)

    class Meta:
        verbose_name = 'Сущность покемона'
        verbose_name_plural = 'Сущности покемонов'

    def __str__(self):
        return f'{self.pokemon.title_ru} {self.level}'
