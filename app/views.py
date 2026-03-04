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
            'name': 'Chronicles of Narnia: The Lion, The Witch, and The Wardrobe',
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



def api_search(request):
    """
    Return search results as JSON for asynchronous requests.
    """
    search_query = request.GET.get('q', '')

    genre_results = []

    for genre_name in LIBRARY.keys():
        match = re.search(re.escape(search_query), genre_name, re.IGNORECASE)
        if match:
            genre_results.append(genre_name)

    print(genre_results)
    results = {
        'query': search_query,
        'genres': genre_results,
    }


    return JsonResponse(results)

'''
def genre_search(request):
    """
    Return search results as JSON for asynchronous requests.
    """
    search_query = request.GET.get('q', '')

    fullResults = []
    genre_results = []
    book_results = []

    for genre_name in LIBRARY.keys():
        match = re.search(search_query, genre_name, re.IGNORECASE)
        if match:
            genre_obj = {
                'genre_name': genre_name,
                'books': []
            }
            for book in LIBRARY[genre_name].values():
                # make a shallow copy to avoid mutating LIBRARY
                book_copy = book.copy()
                book_copy['genre'] = genre_name
                genre_obj['books'].append(book_copy)

            genre_results.append(genre_obj)

    results = {
        'query': search_query,
        'genres': fullResults,
    }
    print(results)

    return JsonResponse(results)

'''
