import django.http.response
import folium
import json

from django.db.models import Prefetch
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import pytz
from .models import Pokemon, PokemonEntity
from datetime import datetime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    now = datetime.now(tz=pytz.UTC)
    pokemons = Pokemon.objects.prefetch_related(
        Prefetch(
            'entities',
            queryset=PokemonEntity.objects.filter(
                appeared_at__lte=now,
                disappeared_at__gte=now,
            ).select_related('pokemon'),
            to_attr='available_entities',
        )
    ).all()

    for pokemon in pokemons:
        for pokemon_entity in pokemon.available_entities:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.photo.url),
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = get_object_or_404(
            Pokemon.objects.select_related(
            'parent',
        ),
            pk=pokemon_id,
        )
    except django.http.response.Http404:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.select_related('pokemon').filter(pokemon=requested_pokemon)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    pokemon = {
        'pokemon_id': requested_pokemon.pk,
        'img_url': request.build_absolute_uri(requested_pokemon.photo.url),
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
    }
    next_evolution = requested_pokemon.next_evolution.first()

    if next_evolution:
        pokemon['next_evolution'] = {
            'pokemon_id': next_evolution.pk,
            'title_ru': next_evolution.title_ru,
            'img_url': request.build_absolute_uri(next_evolution.photo.url),
        }

    previous_evolution = requested_pokemon.parent

    if previous_evolution:
        pokemon['previous_evolution'] = {
            'pokemon_id': previous_evolution.pk,
            'title_ru': previous_evolution.title_ru,
            'img_url': request.build_absolute_uri(previous_evolution.photo.url),
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
