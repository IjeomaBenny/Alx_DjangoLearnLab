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


# Social Media API (Django REST)

Live URL: https://alx-djangolearnlab-y787.onrender.com

## Features
- Custom user (bio, profile_picture, followers/following)
- Token auth (register, login)
- Posts & Comments (CRUD, pagination, search)
- Follows & Feed (posts from followed users)
- Likes
- Notifications (follow, like, comment)

## Quick Start (Local)
```bash
python -m venv venv
venv\Scripts\activate   # on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Auth Endpoints

Register: POST /api/accounts/register/

{ "username": "user", "email": "user@example.com", "password": "StrongPass123!" }


Login: POST /api/accounts/login/

{ "username": "user", "password": "StrongPass123!" }


Profile (auth): GET /api/accounts/profile/
Header: Authorization: Token <token>

Posts & Comments

List/Create posts: GET|POST /api/posts/ (auth for POST)

{ "title": "My post", "content": "Body..." }


Retrieve/Update/Delete post: GET|PATCH|DELETE /api/posts/{id}/ (owner-only for edit/delete)

List/Create comments: GET|POST /api/comments/?post={post_id}

{ "post": 1, "content": "Nice!" }

Follows & Feed (auth)

Follow: POST /api/accounts/follow/{user_id}/

Unfollow: POST /api/accounts/unfollow/{user_id}/

Feed: GET /api/feed/ (posts from followed users; newest first)

Likes (auth)

Like: POST /api/posts/{id}/like/

Unlike: POST /api/posts/{id}/unlike/

PostSerializer includes comments_count and likes_count.

Notifications (auth)

List: GET /api/notifications/

Mark all read: POST /api/notifications/mark-read/

Deployment (Render)

Procfile: web: gunicorn social_media_api.wsgi --log-file -

ENV VARS: SECRET_KEY, DEBUG=False, ALLOWED_HOSTS=.onrender.com,127.0.0.1,localhost, CSRF_TRUSTED_ORIGINS=https://*.onrender.com, DATABASE_URL (Render Postgres), SECURE_SSL_REDIRECT=True, SECURE_HSTS_SECONDS=0

Build cmd: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

Start cmd: gunicorn social_media_api.wsgi --log-file -

Tech

Django 5, DRF, Token Auth

django-filter (search/order), WhiteNoise (static), Gunicorn

Postgres in prod (Render free tier), SQLite in dev