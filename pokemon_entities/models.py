from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    photo = models.ImageField(upload_to='pokemons', null=True, blank=True, verbose_name="Изображение")

    def __str__(self):
        return str(self.title)
