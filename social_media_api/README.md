# Social Media API (Starter)

## Stack
- Django
- Django REST Framework
- Token Authentication

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Posts & Comments API

### Auth
Use header: `Authorization: Token <token>`

### Posts
- **POST** `/api/posts/`  
  Body: `{"title":"First Post","content":"Hello world!"}`
- **GET** `/api/posts/` (paginated)  
  Filters: `?search=<text>` (title/content)  
  Ordering: `?ordering=-created_at` | `?ordering=created_at`
- **GET** `/api/posts/{id}/`
- **PATCH** `/api/posts/{id}/` (owner only)
- **DELETE** `/api/posts/{id}/` (owner only)

### Comments
- **POST** `/api/comments/`  
  Body: `{"post": <POST_ID>, "content": "Nice one!"}`
- **GET** `/api/comments/?post=<POST_ID>` (list for a post)
- **GET** `/api/comments/{id}/`
- **PATCH** `/api/comments/{id}/` (owner only)
- **DELETE** `/api/comments/{id}/` (owner only)


## Follow & Feed

### Follow / Unfollow
- **POST** `/api/accounts/follow/<user_id>/`
- **POST** `/api/accounts/unfollow/<user_id>/`
Requires `Authorization: Token <token>`

### Feed
- **GET** `/api/feed/`
Returns posts by the logged-in user and those they follow, newest first.


