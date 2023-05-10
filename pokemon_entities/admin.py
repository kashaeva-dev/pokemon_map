from django.contrib import admin

from .models import Pokemon, PokemonEntity

class PokemonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'title_en', 'title_jp', 'description')

admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(PokemonEntity)
