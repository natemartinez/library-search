from django.contrib import admin
from .models import Book, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'published_year')
    list_filter = ('genre',)
    search_fields = ('title', 'author')
