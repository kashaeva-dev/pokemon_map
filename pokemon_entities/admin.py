from django.contrib import admin

from .models import Pokemon, PokemonEntity, PokemonElementType


class PokemonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'title_en', 'title_jp', 'photo', 'parent', 'description')


admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(PokemonEntity)
admin.site.register(PokemonElementType)
