from django.contrib import admin
from movies.models import Filmwork, GenreFilmwork, Person, PersonFilmwork

from .models import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline, GenreFilmworkInline,)

    # Отображение полей в списке
    list_display = ('title',
                    'type',
                    'creation_date',
                    'rating',
                    'created',
                    'modified',
                    'file')

    # Фильтрация в списке
    list_filter = ('type',)

    # Поиск по полям
    search_fields = ('title', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)
