"""
Views for the library search application.
"""
from django.shortcuts import render
import re

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


def search(request):
    """
    Handle search requests and display results.
    """
    # Get search parameters from the request
    search_query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'title')  # 'title' or 'genre', 'title' is just the DEFAULT

    print(f"🔍 Search query: '{search_query}'")
    print(f"🔍 Search type: '{search_type}'")

    results = []


    # TODO(human): Implement the search logic
    # Context: You already have find_books() and find_genre() functions in main.py
    # Your Task: Adapt that logic here to search the LIBRARY dictionary
    # Guidance:
    # - If search_type is 'title', search through all book names (use re.search for partial matching)
    # - If search_type is 'genre', search through genre names and return all books in matching genres
    # - Store results as a list of dictionaries: [{'name': '...', 'author': '...', 'genre': '...'}, ...]
    # - Remember to handle the case when search_query is empty

    if search_type == 'title':
        for index, genre in LIBRARY.items():
            for book_id, book in genre.items():
             match = re.search(search_query, book["name"])
             if match:
                results.append(book)

    if search_type == 'genre':
       for genre_name in LIBRARY.keys():
           match = re.search(search_query, genre_name, re.IGNORECASE)
           if match: 
               genre_obj = {
                  'genre_name': genre_name,
                  'books': []
               }
               # results.append(f"{genre_name}") # use multi-line to match pseudocode
               for book in LIBRARY[genre_name].values():     
                   genre_obj['books'].append(book)

               results.append(genre_obj) 
   
    print(results)

    '''
        Results NEEDS TO CHANGE TO DISPLAY EACH GENRE AS A HEADING SEPARATOR:
        This is what should be returned:

        results = [
            genre1: [
                {book1},
                {book2}
            ],       
            genre2: [
                {book1}.
                {book2}
            ]
        
        ]
    
    '''
           

    # Return results to template
    return render(request, 'search_results.html', {
        'query': search_query,
        'search_type': search_type,
        'results': results,
    })
