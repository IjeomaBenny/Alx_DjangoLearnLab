# Models & Serializers (Advanced API Project)

## Models
- **Author**: stores the author's `name`.
- **Book**: stores `title`, `publication_year`, and `author` (FK to Author).
  - Relationship: One `Author` → Many `Book`s (one-to-many).
  - `related_name="books"` on `Book.author` enables reverse access: `author.books`.

## Serializers
- **BookSerializer**
  - Fields: `id`, `title`, `publication_year`, `author`
  - Validation: `publication_year` must not be in the future.
- **AuthorSerializer**
  - Fields: `id`, `name`, `books`
  - Nested: `books` uses `BookSerializer(many=True, read_only=True)` to include all books owned by the author.

## Testing
Use Django shell or admin to create Authors and Books, then serialize them via shell to confirm nested structure and validation.


# Advanced API Project — Models & Serializers

## Models
- **Author**: `name`
- **Book**: `title`, `publication_year`, `author` (FK → Author, `related_name="books"`)

## Serializers
- **BookSerializer**: all fields; validates `publication_year` not in the future.
- **AuthorSerializer**: `id`, `name`, nested `books` via `BookSerializer(many=True, read_only=True)`.

## Quick Test
Use Django shell:
- Create Authors/Books
- Serialize a Book and an Author (shows nested books)
- Validate future-year rejection

## Temporary Endpoint
- `GET /authors/` → lists authors with nested books (for visual inspection)



## Book API Endpoints

| Method | Endpoint                  | Auth Required | Description |
|--------|---------------------------|---------------|-------------|
| GET    | /books/                   | No            | List all books with filters/search/ordering |
| GET    | /books/<id>/              | No            | Retrieve single book by ID |
| POST   | /books/create/            | Yes           | Create a new book |
| PATCH  | /books/<id>/update/       | Yes           | Update a book (partial) |
| PUT    | /books/<id>/update/       | Yes           | Update a book (full) |
| DELETE | /books/<id>/delete/       | Yes           | Delete a book |

### Permissions
- **Unauthenticated users** → can only GET list/detail
- **Authenticated users** → can POST, PATCH/PUT, DELETE

### Validation
- `publication_year` cannot be in the future (enforced in serializer).


## Filtering, Searching, Ordering

### Filtering
- `?title=<substring>` (icontains)
- `?author=<id>`
- `?publication_year=<year>`
- `?min_year=<year>&max_year=<year>`

### Search
- `?search=<text>` across `title` and `author__name`

### Ordering
- `?ordering=publication_year` or `?ordering=-publication_year`

