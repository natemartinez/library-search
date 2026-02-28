from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books')
    published_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    cover_color = models.CharField(
        max_length=7, blank=True,
        help_text='Hex color for book spine, e.g. #ff0000'
    )

    def __str__(self):
        return f"{self.title} — {self.author}"
