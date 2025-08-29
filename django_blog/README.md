# Authentication — django_blog

## Features
- Register (username, email, password) — /register
- Login — /login
- Logout — /logout
- View profile — /profile (login required)
- Edit profile (first_name, last_name, email) — /profile/edit (POST updates; login required)

## How it works
- Forms: `RegisterForm` (extends `UserCreationForm`), `ProfileForm` (ModelForm for `User`)
- Views:
  - `register` — creates user, logs them in, redirects to `profile`
  - `profile` — shows current user info
  - `profile_edit` — GET shows form; POST saves changes, redirects to `profile`
- URLs:
  - `login/`, `logout/` use Django auth views with custom templates
  - `register/`, `profile/`, `profile/edit/` are custom views
- Templates:
  - `registration/login.html`, `registration/logout.html`, `registration/register.html`
  - `blog/profile.html`, `blog/profile_edit.html`, `blog/base.html`
- Security:
  - All POST forms include `{% csrf_token %}`
  - `@login_required` protects `/profile` and `/profile/edit`
  - Passwords hashed by Django

## Testing
1. Run server: `python manage.py runserver`
2. Go to `/register` → create user → redirected to `/profile`
3. `/logout` then `/login`
4. `/profile/edit/` → update details → redirected with success message
5. While logged out, try `/profile` → should redirect to `/login?next=/profile`
