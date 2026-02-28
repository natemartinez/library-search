# Library Search Application - Development Plan

## 1. PROJECT VISION & GOALS

### Overview
A Django-based digital library application where users can browse, search, and interact with books using an intuitive 3D visual interface.

### Core Goals
- **MVP**: Functional book search with visual 3D book model display
- **UX**: Engaging 3D CSS-based book shelf interface
- **Database**: Persistent storage of library data (migrate from hardcoded LIBRARY dict)
- **Scalability**: Structure for API integration and future features

### Success Metrics
- Users can search books by title, author, genre
- 3D book models render correctly on home/search pages
- Add-to-favorites functionality works
- Clean, maintainable codebase

---

## 2. ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML/CSS/JS)               │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Home Page       │  Search Results  │  Favorites │   │
│  │  - 3D Bookshelf  │  - Book Grid     │  - My List │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP Requests
┌──────────────────────▼──────────────────────────────────┐
│              DJANGO APPLICATION LAYER                   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Views (home, search, api_endpoints)              │   │
│  │ Forms (search filters)                           │   │
│  │ Context Processors (available genres/stats)      │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │ ORM Queries
┌──────────────────────▼──────────────────────────────────┐
│              DATABASE LAYER (SQLite)                     │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Book (id, title, author, genre, published_year) │   │
│  │ Genre (id, name)                                 │   │
│  │ UserFavorite (user, book, added_at)              │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 3. DATABASE SCHEMA

### Models to Create

**Book**
- id (PrimaryKey)
- title (CharField, max_length=255)
- author (CharField, max_length=255)
- genre (ForeignKey → Genre)
- published_year (IntegerField, optional)
- description (TextField, optional)
- cover_color (CharField, for 3D styling) - hex color for book spine

**Genre**
- id (PrimaryKey)
- name (CharField, unique=True)

**UserFavorite** (Future feature)
- id (PrimaryKey)
- user (ForeignKey → User)
- book (ForeignKey → Book)
- added_at (DateTimeField, auto_now_add=True)

---

## 4. FEATURE BREAKDOWN

### Phase 1: MVP (Current Focus)
- [x] Django project setup
- [ ] **Book Model & Database**
  - Create models.py with Book, Genre
  - Create migrations
  - Migrate data from hardcoded LIBRARY dict
- [ ] **3D Book CSS Component**
  - CSS 3D transforms for book model
  - Reusable book component
  - Test on home page
- [ ] **Search Functionality**
  - Update views.py to query database
  - Implement search filters
  - Display results with 3D books
- [ ] **Templates Update**
  - home.html - bookshelf grid
  - search_results.html - result grid
  - Components - single book (3D model)

### Phase 2: Enhanced Features
- [ ] User authentication & favorites
- [ ] Genre page (view all books in genre)
- [ ] Book detail page
- [ ] Advanced search filters
- [ ] Sort options (title, author, year)

### Phase 3: Polish & Scale
- [ ] API endpoints (JSON responses)
- [ ] Loading states & error handling
- [ ] Mobile responsiveness
- [ ] Performance optimization
- [ ] Admin panel customization

---

## 5. IMPLEMENTATION ROADMAP

### Sprint 1: Database & Models (Week 1)
**Goal**: Get books in database, remove hardcoded data

Tasks:
1. Create `models.py` with Book & Genre models
2. Create initial migration
3. Write data migration to populate books from LIBRARY dict
4. Create admin.py for admin panel management
5. Test: `python manage.py shell` and verify books exist

**Deliverable**: Working Book/Genre models, populated database

### Sprint 2: 3D Book Component (Week 2)
**Goal**: Design and implement CSS 3D book model

Tasks:
1. Research CSS 3D transforms (perspective, rotateY, etc.)
2. Create `static/css/book-3d.css` with book styles
3. Create book.html template component
4. Test on home page - render 5 sample books
5. Refine styling (shadows, colors, responsiveness)

**Deliverable**: Reusable 3D book component, CSS file, visual feedback

### Sprint 3: Search & Views (Week 3)
**Goal**: Connect database to search functionality

Tasks:
1. Update `views.py` - query database instead of dict
2. Implement search filter logic (title, author, genre)
3. Update `search_results.html` to display books with 3D models
4. Update `home.html` to show genre browsing
5. Test search functionality

**Deliverable**: Functional search, updated templates

### Sprint 4: Polish & Testing (Week 4)
**Goal**: Refine UX, fix bugs, document

Tasks:
1. User testing - find UX issues
2. Bug fixes
3. Mobile responsiveness
4. Code cleanup & comments
5. Document setup in README

**Deliverable**: Polished MVP, README with setup instructions

---

## 6. CURRENT STATE → NEXT STEPS

### What You Have Now
✅ Django project structure  
✅ Basic views (home, search)  
✅ Hardcoded book data (LIBRARY dict)  
✅ Template files exist  
✅ SQLite database ready  

### Immediate Next Actions (Priority Order)
1. **Create models.py** - Book & Genre models
2. **Run migrations** - Set up database tables
3. **Populate database** - Move LIBRARY data into DB
4. **Create CSS 3D book** - Design the component
5. **Update views** - Query DB instead of dict

---

## 7. KEY DECISIONS MADE

| Decision | Choice | Why |
|----------|--------|-----|
| Database | SQLite (Django default) | Good for MVP, easy to migrate later |
| 3D Approach | CSS 3D (not WebGL) | Lightweight, fast, no external libs |
| User Auth | Defer to Phase 2 | Keep MVP simple, focus on core features |
| Data Source | Local DB first | Foundation for future API integration |
| Templates | Django template language | Already setup, simple for this project |

---

## 8. DEVELOPER SKILL FOCUS

As a Jr→Mid developer, this project helps you learn:
- **Architecture**: Breaking features into layers (models → views → templates)
- **Database Design**: Creating normalized schemas, migrations
- **Feature Planning**: Breaking work into sprints with clear deliverables
- **Testing Mindset**: Each sprint has a concrete "works" criteria
- **Code Organization**: Separating concerns (CSS, models, views, templates)

### Practice Planning Skills Here:
✅ Write user-facing features first, then break into tasks  
✅ Define "done" for each sprint (deliverables)  
✅ Create architecture before coding  
✅ Track dependencies (models before views, CSS before templates need it)  

---

## 9. NOTES & BLOCKERS

- None currently - project is clear to start
- Monitor scope creep: stick to MVP in Phase 1
- Test frequently to catch bugs early

---

**Last Updated**: February 26, 2026  
**Status**: Ready for Sprint 1 (Database & Models) 
     