"""
Views for the library search application.
"""
from django.shortcuts import render
from django.http import JsonResponse
import re

# Spine color palette per genre — bg, accent stripe, text, muted text
GENRE_SPINE_COLORS = {
    'Science Fiction':  {'bg': '#1A1A2E', 'accent': '#3C3489', 'text': '#AFA9EC', 'muted_text': '#4A4060'},
    'Fantasy':          {'bg': '#1A2E1C', 'accent': '#2D5E3A', 'text': '#5DCAA5', 'muted_text': '#2A4A30'},
    'Fiction':          {'bg': '#2A1A10', 'accent': '#993C1D', 'text': '#F09595', 'muted_text': '#5A2020'},
    'Mystery':          {'bg': '#1C1810', 'accent': '#854F0B', 'text': '#EF9F27', 'muted_text': '#5A4A20'},
    'Romance':          {'bg': '#2A1020', 'accent': '#72243E', 'text': '#F0A5C5', 'muted_text': '#5A2040'},
    'Horror':           {'bg': '#1A0A0A', 'accent': '#712B13', 'text': '#E87070', 'muted_text': '#4A1A1A'},
    'Non-Fiction':      {'bg': '#1C2010', 'accent': '#3B6D11', 'text': '#8FCA5A', 'muted_text': '#2A4010'},
    'Biography':        {'bg': '#202020', 'accent': '#444441', 'text': '#AAAAAA', 'muted_text': '#444441'},
    'Thriller':         {'bg': '#0A0A1C', 'accent': '#185FA5', 'text': '#7DB8F0', 'muted_text': '#1A2A4A'},
    'Historical Fiction':{'bg': '#1C180A', 'accent': '#7A6210', 'text': '#D4B85A', 'muted_text': '#4A3A10'},
}

# Width/height pairs (px) for the visual bookshelf — one per genre slot
SPINE_DIMENSIONS = [
    (17, 67), (21, 56), (14, 76), (18, 50), (16, 78),
    (22, 61), (14, 53), (18, 70), (17, 59), (20, 81),
]

# Library data (from main.py prototype)
# Later, this needs to be a database model in `models.py`
LIBRARY = {
    'Science Fiction': {
        'book1': {
            'name': 'The Hunger Games',
            'author': 'Suzanne Collins',
            'cover': '/static/images/placeholder.jpg',
        },
        'book2': {
            'name': 'Divergent',
            'author': 'Veronica Roth',
            'cover': '/static/images/placeholder.jpg',
        },
        'book3': {
            'name': 'Ender\'s Game',
            'author': 'Orson Scott Card',
            'cover': '/static/images/placeholder.jpg',
        },
        'book4': {
            'name': 'Dune',
            'author': 'Frank Herbert',
            'cover': '/static/images/placeholder.jpg',
        },
        'book5': {
            'name': 'The Martian',
            'author': 'Andy Weir',
            'cover': '/static/images/placeholder.jpg',
        },
        'book6': {
            'name': 'Fahrenheit 451',
            'author': 'Ray Bradbury',
            'cover': '/static/images/placeholder.jpg',
        },
        'book7': {
            'name': 'Brave New World',
            'author': 'Aldous Huxley',
            'cover': '/static/images/placeholder.jpg',
        },
        'book8': {
            'name': 'The Left Hand of Darkness',
            'author': 'Ursula K. Le Guin',
            'cover': '/static/images/placeholder.jpg',
        },
    },
    'Fantasy': {
        'book1': {
            'name': 'Lord of the Rings',
            'author': 'J.R Tolkein',
            'cover': '/static/images/placeholder.jpg',
        },
        'book2': {
            'name': 'The Chronicles of Narnia: The Lion, The Witch, and The Wardrobe',
            'author': 'C.S Lewis',
            'cover': '/static/images/placeholder.jpg',
        },
        'book3': {
            'name': 'Harry Potter and the Sorcerer\'s Stone',
            'author': 'J.K. Rowling',
            'cover': '/static/images/placeholder.jpg',
        },
        'book4': {
            'name': 'The Name of the Wind',
            'author': 'Patrick Rothfuss',
            'cover': '/static/images/placeholder.jpg',
        },
        'book5': {
            'name': 'A Game of Thrones',
            'author': 'George R.R. Martin',
            'cover': '/static/images/placeholder.jpg',
        },
        'book6': {
            'name': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'cover': '/static/images/placeholder.jpg',
        },
        'book7': {
            'name': 'American Gods',
            'author': 'Neil Gaiman',
            'cover': '/static/images/placeholder.jpg',
        },
        'book8': {
            'name': 'The Way of Kings',
            'author': 'Brandon Sanderson',
            'cover': '/static/images/placeholder.jpg',
        },
    },
    'Fiction': {
        'book1': {
            'name': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'cover': '/static/images/placeholder.jpg',
        },
        'book2': {
            'name': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'cover': '/static/images/placeholder.jpg',
        },
        'book3': {
            'name': '1984',
            'author': 'George Orwell',
            'cover': '/static/images/placeholder.jpg',
        },
        'book4': {
            'name': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'cover': '/static/images/placeholder.jpg',
        },
        'book5': {
            'name': 'Of Mice and Men',
            'author': 'John Steinbeck',
            'cover': '/static/images/placeholder.jpg',
        },
        'book6': {
            'name': 'Beloved',
            'author': 'Toni Morrison',
            'cover': '/static/images/placeholder.jpg',
        },
        'book7': {
            'name': 'One Hundred Years of Solitude',
            'author': 'Gabriel García Márquez',
            'cover': '/static/images/placeholder.jpg',
        },
        'book8': {
            'name': 'Slaughterhouse-Five',
            'author': 'Kurt Vonnegut',
            'cover': '/static/images/placeholder.jpg',
        },
    },
    'Mystery': {
        'book1': {
            'name': 'The Hound of the Baskervilles',
            'author': 'Arthur Conan Doyle',
            'cover': '/static/images/placeholder.jpg',
        },
        'book2': {
            'name': 'And Then There Were None',
            'author': 'Agatha Christie',
            'cover': '/static/images/placeholder.jpg',
        },
        'book3': {
            'name': 'Gone Girl',
            'author': 'Gillian Flynn',
            'cover': '/static/images/placeholder.jpg',
        },
        'book4': {
            'name': 'The Girl with the Dragon Tattoo',
            'author': 'Stieg Larsson',
            'cover': '/static/images/placeholder.jpg',
        },
        'book5': {
            'name': 'In the Woods',
            'author': 'Tana French',
            'cover': '/static/images/placeholder.jpg',
        },
        'book6': {
            'name': 'Big Little Lies',
            'author': 'Liane Moriarty',
            'cover': '/static/images/placeholder.jpg',
        },
        'book7': {
            'name': 'The Murder of Roger Ackroyd',
            'author': 'Agatha Christie',
            'cover': '/static/images/placeholder.jpg',
        },
        'book8': {
            'name': 'Sharp Objects',
            'author': 'Gillian Flynn',
            'cover': '/static/images/placeholder.jpg',
        },
    },
    'Romance': {
        'book1': {
            'name': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'cover': '/static/images/placeholder.jpg',
        },
        'book2': {
            'name': 'The Notebook',
            'author': 'Nicholas Sparks',
            'cover': '/static/images/placeholder.jpg',
        },
        'book3': {
            'name': 'Outlander',
            'author': 'Diana Gabaldon',
            'cover': '/static/images/placeholder.jpg',
        },
        'book4': {
            'name': 'Me Before You',
            'author': 'Jojo Moyes',
            'cover': '/static/images/placeholder.jpg',
        },
        'book5': {
            'name': 'The Hating Game',
            'author': 'Sally Thorne',
            'cover': '/static/images/placeholder.jpg',
        },
        'book6': {
            'name': 'It Ends with Us',
            'author': 'Colleen Hoover',
            'cover': '/static/images/placeholder.jpg',
        },
        'book7': {
            'name': 'Sense and Sensibility',
            'author': 'Jane Austen',
            'cover': '/static/images/placeholder.jpg',
        },
        'book8': {
            'name': 'The Time Traveler\'s Wife',
            'author': 'Audrey Niffenegger',
            'cover': '/static/images/placeholder.jpg',
        },
    },
    'Horror': {
        'book1': {
            'name': 'The Shining',
            'author': 'Stephen King',
            'cover': '/static/images/placeholder.jpg',
        },
        'book2': {
            'name': 'Dracula',
            'author': 'Bram Stoker',
            'cover': '/static/images/placeholder.jpg',
        },
        'book3': {
            'name': 'Frankenstein',
            'author': 'Mary Shelley',
            'cover': '/static/images/placeholder.jpg',
        },
        'book4': {
            'name': 'It',
            'author': 'Stephen King',
            'cover': '/static/images/placeholder.jpg',
        },
        'book5': {
            'name': 'Pet Sematary',
            'author': 'Stephen King',
            'cover': '/static/images/placeholder.jpg',
        },
        'book6': {
            'name': 'House of Leaves',
            'author': 'Mark Z. Danielewski',
            'cover': '/static/images/placeholder.jpg',
        },
        'book7': {
            'name': 'The Haunting of Hill House',
            'author': 'Shirley Jackson',
            'cover': '/static/images/placeholder.jpg',
        },
        'book8': {
            'name': 'Interview with the Vampire',
            'author': 'Anne Rice',
            'cover': '/static/images/placeholder.jpg',
        },
    },
    'Non-Fiction': {
        'book1': {
            'name': 'Sapiens: A Brief History of Humankind',
            'author': 'Yuval Noah Harari',
            'cover': '/static/images/placeholder.jpg',
        },
        'book2': {
            'name': 'Educated',
            'author': 'Tara Westover',
            'cover': '/static/images/placeholder.jpg',
        },
        'book3': {
            'name': 'The Immortal Life of Henrietta Lacks',
            'author': 'Rebecca Skloot',
            'cover': '/static/images/placeholder.jpg',
        },
        'book4': {
            'name': 'Becoming',
            'author': 'Michelle Obama',
            'cover': '/static/images/placeholder.jpg',
        },
        'book5': {
            'name': 'The Power of Habit',
            'author': 'Charles Duhigg',
            'cover': '/static/images/placeholder.jpg',
        },
        'book6': {
            'name': 'Outliers',
            'author': 'Malcolm Gladwell',
            'cover': '/static/images/placeholder.jpg',
        },
        'book7': {
            'name': 'The Body: A Guide for Occupants',
            'author': 'Bill Bryson',
            'cover': '/static/images/placeholder.jpg',
        },
        'book8': {
            'name': 'Thinking, Fast and Slow',
            'author': 'Daniel Kahneman',
            'cover': '/static/images/placeholder.jpg',
        },
    },
    'Biography': {
        'book1': {
            'name': 'Steve Jobs',
            'author': 'Walter Isaacson',
            'cover': '/static/images/placeholder.jpg',
        },
        'book2': {
            'name': 'The Diary of a Young Girl',
            'author': 'Anne Frank',
            'cover': '/static/images/placeholder.jpg',
        },
        'book3': {
            'name': 'Long Walk to Freedom',
            'author': 'Nelson Mandela',
            'cover': '/static/images/placeholder.jpg',
        },
        'book4': {
            'name': 'I Know Why the Caged Bird Sings',
            'author': 'Maya Angelou',
            'cover': '/static/images/placeholder.jpg',
        },
        'book5': {
            'name': 'The Story of My Experiments with Truth',
            'author': 'Mahatma Gandhi',
            'cover': '/static/images/placeholder.jpg',
        },
        'book6': {
            'name': 'Alexander Hamilton',
            'author': 'Ron Chernow',
            'cover': '/static/images/placeholder.jpg',
        },
        'book7': {
            'name': 'Leonardo da Vinci',
            'author': 'Walter Isaacson',
            'cover': '/static/images/placeholder.jpg',
        },
        'book8': {
            'name': 'The Story of a New Name',
            'author': 'Elena Ferrante',
            'cover': '/static/images/placeholder.jpg',
        },
    },
    'Thriller': {
        'book1': {
            'name': 'The Da Vinci Code',
            'author': 'Dan Brown',
            'cover': '/static/images/placeholder.jpg',
        },
        'book2': {
            'name': 'The Silence of the Lambs',
            'author': 'Thomas Harris',
            'cover': '/static/images/placeholder.jpg',
        },
        'book3': {
            'name': 'No Country for Old Men',
            'author': 'Cormac McCarthy',
            'cover': '/static/images/placeholder.jpg',
        },
        'book4': {
            'name': 'The Bourne Identity',
            'author': 'Robert Ludlum',
            'cover': '/static/images/placeholder.jpg',
        },
        'book5': {
            'name': 'The Girl on the Train',
            'author': 'Paula Hawkins',
            'cover': '/static/images/placeholder.jpg',
        },
        'book6': {
            'name': 'Before I Go to Sleep',
            'author': 'S.J. Watson',
            'cover': '/static/images/placeholder.jpg',
        },
        'book7': {
            'name': 'I Am Pilgrim',
            'author': 'Terry Hayes',
            'cover': '/static/images/placeholder.jpg',
        },
        'book8': {
            'name': 'The Woman in the Window',
            'author': 'A.J. Finn',
            'cover': '/static/images/placeholder.jpg',
        },
    },
    'Historical Fiction': {
        'book1': {
            'name': 'All the Light We Cannot See',
            'author': 'Anthony Doerr',
            'cover': '/static/images/placeholder.jpg',
        },
        'book2': {
            'name': 'The Pillars of the Earth',
            'author': 'Ken Follett',
            'cover': '/static/images/placeholder.jpg',
        },
        'book3': {
            'name': 'The Book Thief',
            'author': 'Markus Zusak',
            'cover': '/static/images/placeholder.jpg',
        },
        'book4': {
            'name': 'Wolf Hall',
            'author': 'Hilary Mantel',
            'cover': '/static/images/placeholder.jpg',
        },
        'book5': {
            'name': 'The Kite Runner',
            'author': 'Khaled Hosseini',
            'cover': '/static/images/placeholder.jpg',
        },
        'book6': {
            'name': 'Memoirs of a Geisha',
            'author': 'Arthur Golden',
            'cover': '/static/images/placeholder.jpg',
        },
        'book7': {
            'name': 'Roots',
            'author': 'Alex Haley',
            'cover': '/static/images/placeholder.jpg',
        },
        'book8': {
            'name': 'Lincoln',
            'author': 'Gore Vidal',
            'cover': '/static/images/placeholder.jpg',
        },
    },
}

def _build_currently_reading():
    """Shared context for the currently-reading book (used by Home and The Desk)."""
    genres = list(LIBRARY.items())
    first_genre, first_books = genres[0]
    first_book = list(first_books.values())[0]
    cr_colors = GENRE_SPINE_COLORS.get(first_genre, {})
    return {
        'name': first_book['name'],
        'author': first_book['author'],
        'chapter': 7,
        'total_chapters': 20,
        'chapter_title': 'The Secret to Self-Control',
        'chapter_quote': "It is easier to practice restraint when you don\u2019t have to use it very often.",
        'page': 94,
        'total_pages': 271,
        'progress': 35,
        'title_abbr': ' '.join(first_book['name'].upper().split()[:3]),
        'author_abbr': first_book['author'].upper().split()[-1],
        'bg': cr_colors.get('bg', '#1A2E1C'),
        'accent': cr_colors.get('accent', '#C4842A'),
        'text': cr_colors.get('text', '#9B7A3E'),
    }

def stacks(request):
    genres = list(LIBRARY.items())
    stacks = []
    all_books = []

    for i, (genre, books) in enumerate(genres):
        colors = GENRE_SPINE_COLORS.get(genre, {'bg': '#1C1810', 'accent': '#854F0B', 'text': '#EF9F27', 'muted_text': '#5A4A20'})
        w, h = SPINE_DIMENSIONS[i % len(SPINE_DIMENSIONS)]

        # stacks: one spine per genre (first book only)
        if i < len(SPINE_DIMENSIONS):
            first_book = list(books.values())[0]
            stacks.append({
                'name': first_book['name'],
                'author': first_book['author'],
                'title_abbr': ' '.join(first_book['name'].upper().split()[:3]),
                'author_abbr': first_book['author'].upper().split()[-1],
                'width': w,
                'height': h,
                'is_current': i == 0,
                **colors,
            })

        # all_books: every book in the library with genre + dimensions
        for book in books.values():
            all_books.append({
                'name': book['name'],
                'author': book['author'],
                'genre': genre,
                'title_abbr': ' '.join(book['name'].upper().split()[:3]),
                'author_abbr': book['author'].upper().split()[-1],
                'width': w,
                'height': h,
                **colors,
            })

    currently_reading = _build_currently_reading()

    stats = {
        'volumes': len(stacks),
        'notes': 43,
        'relics': 7,
        'days_read': 12,
        'in_progress': 2,
    }

    return render(request, 'home.html', {
        'stacks': stacks,
        'currently_reading': currently_reading,
        'stats': stats,
        'all_books': all_books,
        'total': len(all_books),
        'genres': list(LIBRARY.keys()),
    })

def storyboard(request):
    connections = [
        {
            'book_a': 'The Hunger Games',
            'book_b': 'Dune',
            'tag': 'Power & Control',
            'note': 'Both explore authoritarian regimes and rebellion.',
            'confirmed': True,
        },
        {
            'book_a': 'The Hunger Games',
            'book_b': '1984',
            'tag': 'Dystopian Society',
            'note': 'Both depict oppressive governments and surveillance.',
            'confirmed': False,
        },
    ]
    return render(request, 'storyboard.html', {'connections': connections})

def acquisitions(request):
    new_arrivals = []
    for genre, books in LIBRARY.items():
        colors = GENRE_SPINE_COLORS.get(genre, {'bg': '#1C1810', 'accent': '#854F0B', 'text': '#EF9F27', 'muted_text': '#5A4A20'})
        for book in list(books.values())[:2]:
            new_arrivals.append({
                'name': book['name'],
                'author': book['author'],
                'title_abbr': ' '.join(book['name'].upper().split()[:3]),
                'author_abbr': book['author'].upper().split()[-1],
                **colors,
            })
    return render(request, 'acquisitions.html', {'new_arrivals': new_arrivals})

def build_library(request):
    all_books = []
    for i, (genre, books) in enumerate(LIBRARY.items()):
        colors = GENRE_SPINE_COLORS.get(genre, {'bg': '#1C1810', 'accent': '#854F0B', 'text': '#EF9F27', 'muted_text': '#5A4A20'})
        w, h = SPINE_DIMENSIONS[i % len(SPINE_DIMENSIONS)]
        for book in books.values():
            all_books.append({
                'name': book['name'],
                'author': book['author'],
                'genre': genre,
                'title_abbr': ' '.join(book['name'].upper().split()[:3]),
                'author_abbr': book['author'].upper().split()[-1],
                'width': w,
                'height': h,
                **colors,
            })
    return render(request, 'library.html', {
        'all_books': all_books,
        'total': len(all_books),
        'genres': list(LIBRARY.keys()),
    })

def the_desk(request):
    bookmarks = [
        {'icon': '🔍', 'name': 'The Magnifier',     'desc': 'Surfaces recurring patterns and motifs across all your annotations in this book.',      'state': 'act', 'label': 'Active'},
        {'icon': '🧵', 'name': 'The Red Thread',     'desc': 'Links a passage in this book to an idea from another book in your library.',            'state': 'act', 'label': 'Active'},
        {'icon': '📄', 'name': 'The Blank Page',     'desc': 'Sends a chapter prompt to your desk. Designed to be answered on paper first.',          'state': 'act', 'label': 'Active'},
        {'icon': '✏️', 'name': 'The Marginalia',     'desc': 'Tag any passage: Question, Insight, Quote, or Contradiction.',                          'state': 'act', 'label': 'Active'},
        {'icon': '🔒', 'name': 'The Lantern',        'desc': 'Log 10 annotations to discover this. Illuminates related books.',                       'state': 'prg', 'label': '7 / 10'},
        {'icon': '🔒', 'name': 'The Pressed Flower', 'desc': 'Finish your first book to unlock memory prompts.',                                      'state': 'lk',  'label': 'Locked'},
        {'icon': '🔒', 'name': 'The Cipher',         'desc': 'Write your first Desk entry to discover this concept-decoding tool.',                   'state': 'lk',  'label': 'Locked'},
        {'icon': '🔒', 'name': 'The Seal',           'desc': 'Finish your first book to unlock the closing ritual and formal archive entry.',          'state': 'lk',  'label': 'Locked'},
    ]
    return render(request, 'the_desk.html', {
        'currently_reading': _build_currently_reading(),
        'bookmarks': bookmarks,
    })  

def relics(request):
    relics_list = [
        {
            'name': 'The Inkwell',
            'icon': '🖋',
            'origin': 'Found after writing three pages at the Desk in one session.',
            'date': 'March 2026',
            'found': True,
        },
        {
            'name': 'The Dog-Ear',
            'icon': '📖',
            'hint': 'Complete your first paperback to find this.',
            'found': False,
        },
        {
            'name': 'The Foxed Page',
            'icon': '🍂',
            'hint': 'Connect three books in the Archive to find this.',
            'found': False,
        },
        {
            'name': 'The Letter Opener',
            'icon': '✉️',
            'hint': 'Seal your first book to find this.',
            'found': False,
        },
    ]
    return render(request, 'relics.html', {'relics': relics_list})

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
