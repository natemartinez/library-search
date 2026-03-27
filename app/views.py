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

def home(request):

    return render(request, 'home.html', {
        'library': LIBRARY
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


def book_carousel(request):
    all_books = []

    for genre_name, books in LIBRARY.items():
        for book in books.items():
            all_books.append(book)
    
    results = {
        'books': all_books
    }

    return JsonResponse(results)
