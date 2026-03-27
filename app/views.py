"""
Views for the library search application.
"""
from django.shortcuts import render
from django.http import JsonResponse
import re
import asyncio
# Library data (from main.py prototype)
# Later, this needs to be a database model in `models.py`
# from an API maybe?
LIBRARY = {
    'Science Fiction': {
        'book1': {
            'name': 'The Hunger Games',
            'author': 'Suzanne Collins',
        },
        'book2': {
            'name': 'Divergent',
            'author': 'Veronica Roth',
        },
    },
    'Fantasy': {
        'book1': {
            'name': 'Lord of the Rings',
            'author': 'J.R Tolkein',
        },
        'book2': {
            'name': 'The Chronicles of Narnia: The Lion, The Witch, and The Wardrobe',
            'author': 'C.S Lewis',
        },
    },
    'Fiction': {
        'book1': {
            'name': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald'
        }
    }
}


def home(request):
    """
    Display the home page with search form.
    """
    return render(request, 'home.html', {
        'genres': LIBRARY.keys()
    })

def sidebar(request):
    """
    Display the sidebar page.
    """
    return render(request, 'sidebar.html')

def api_search(request):

    search_query = request.GET.get('q', '')

    genre_results = []
    book_results = []

    for genre_name in LIBRARY.keys():
        match = re.search(r'\b' + re.escape(search_query), genre_name, re.IGNORECASE)
        if match:
            genre_results.append(genre_name)
    

    for genre_name, books in LIBRARY.items():
        for book in books.values():
            match = re.search(r'^' + re.escape(search_query), book['name'], re.IGNORECASE) if book['name'] else None
            if match:
                book_results.append(book)


    results = {
        'query': search_query,
        'genres': genre_results,
        'books': book_results
    }


    return JsonResponse(results)
