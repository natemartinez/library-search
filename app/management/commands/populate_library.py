from django.core.management.base import BaseCommand
from app.models import Genre, Book
from app import views


class Command(BaseCommand):
    help = 'Populate the database with books defined in views.LIBRARY'

    def handle(self, *args, **options):
        lib = getattr(views, 'LIBRARY', None)
        if not lib:
            self.stdout.write(self.style.ERROR('LIBRARY constant not found in app.views'))
            return

        total_genres = 0
        total_books = 0

        for genre_name, books in lib.items():
            genre_obj, created = Genre.objects.get_or_create(name=genre_name)
            if created:
                total_genres += 1
            for book_key, data in books.items():
                title = data.get('name')
                author = data.get('author')
                # style: cover_color can be assigned randomly later
                book_obj, book_created = Book.objects.get_or_create(
                    title=title,
                    author=author,
                    genre=genre_obj,
                )
                if book_created:
                    total_books += 1
        self.stdout.write(self.style.SUCCESS(
            f'Populated {total_genres} genres and {total_books} books'
        ))
