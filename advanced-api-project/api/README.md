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


