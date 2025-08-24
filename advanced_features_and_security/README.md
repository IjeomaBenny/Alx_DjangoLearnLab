# Advanced Features & Security – Permissions & Groups

This project demonstrates how to implement role-based access control in Django using **custom permissions** and **groups**.

## Stack
- Django
- Custom User Model: `bookshelf.CustomUser` (via `AUTH_USER_MODEL`)
- App with permissions: `bookshelf` (model: `Book`)

## Custom Permissions
Defined in `bookshelf/models.py` on the `Book` model:

- `can_view` – view the book list/detail
- `can_create` – create a book
- `can_edit` – edit a book
- `can_delete` – delete a book

Example (in `Book.Meta.permissions`):
```python
class Meta:
    permissions = [
        ("can_view", "Can view book"),
        ("can_create", "Can create book"),
        ("can_edit", "Can edit book"),
        ("can_delete", "Can delete book"),
    ]
Groups
Created in Django Admin → Authentication and Authorization → Groups:

Viewers: can_view

Editors: can_view, can_create, can_edit

Admins: all permissions (or make user a superuser)

Assign users to these groups in Admin → Users → change user → Groups.

Views Protection
Views are protected with @permission_required:

book_list → bookshelf.can_view

book_create → bookshelf.can_create

book_edit → bookshelf.can_edit

book_delete → bookshelf.can_delete

If a user lacks a permission, a 403 is raised or they’re redirected to login (based on settings).

URLs & Templates
/books/ – list books (requires can_view)

Optionally add create/edit/delete URLs if used.

Templates under templates/bookshelf/ (e.g., book_list.html).

Settings
In LibraryProject/settings.py:

python
Copy
Edit
AUTH_USER_MODEL = 'bookshelf.CustomUser'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'book_list'
LOGOUT_REDIRECT_URL = 'login'
How to Run
bash
Copy
Edit
# from project folder
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Open:

http://127.0.0.1:8000/login/ to log in

http://127.0.0.1:8000/books/ to view protected list

Testing Permissions (manual)
In Admin:

Create groups (Viewers, Editors, Admins) and assign the permissions above.

Create 2–3 test users and assign each to a different group.

Log in as each user and try:

Viewing books (/books/) – Viewers/Editors/Admins should succeed.

Creating/editing/deleting – only users with can_create / can_edit / can_delete should succeed.

Files Touched for This Task
bookshelf/models.py – added Meta.permissions

bookshelf/views.py – added @permission_required(...) decorators

bookshelf/admin.py – registered models & custom user admin

LibraryProject/settings.py – AUTH_USER_MODEL + auth redirects

templates/bookshelf/*.html – simple pages for testing

yaml
Copy
Edit

---

## commit & push (from your repo root)
Run these exactly:

cd C:\Users\hp\Desktop\Alx_DjangoLearnLab
git add advanced_features_and_security/README.md
git commit -m "Docs: permissions & groups setup, testing steps, and configuration"
git push origin main