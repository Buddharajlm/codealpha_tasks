# Mini Social Media App

A small full-stack social media platform where users can create profiles, share posts, comment, like, and follow each other. Built with Django on the backend and plain HTML, CSS, and JavaScript on the frontend.

## Features

- **User accounts:** registration, login, and logout with securely hashed passwords
- **Profiles:** editable bio, avatar initial, and post, follower, and following counts
- **Posts:** create and delete posts (up to 280 characters), newest first
- **Comments:** add and delete comments on any post
- **Likes:** like and unlike posts with live counts
- **Follow system:** follow and unfollow users, with a personalized **Following** feed alongside an **Everyone** feed
- **User search:** find people by username

## Tech Stack

| Part | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript (no frameworks) |
| Backend | Django (Python) |
| Database | SQLite (users, posts, comments, likes, follows) |
| Auth | Django session authentication with CSRF protection |

## Database Models

- `User` (Django built-in) and `Profile` (bio, avatar)
- `Post`: author, content, created time
- `Comment`: post, author, content
- `Like`: user and post (unique together)
- `Follow`: follower and following (unique together)

## Project Structure

```
minisocial/
├── manage.py
├── config/          # project settings and root URLs
└── core/            # main app
    ├── models.py
    ├── views.py     # pages and JSON API
    ├── urls.py
    ├── templates/   # login, register, home, profile pages
    └── static/core/ # JavaScript and CSS
```

## How to Run Locally

1. Clone the repository and open the project folder:

```bash
   git clone https://github.com/Buddharajlm/codealpha_tasks.git
   cd codealpha_tasks/minisocial
```

2. Create and activate a virtual environment:

```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
```

3. Install the dependencies:

```bash
   pip install -r requirements.txt
```

4. Create the database tables:

```bash
   python manage.py migrate
```

5. Start the server:

```bash
   python manage.py runserver
```

6. Open **http://127.0.0.1:8000** in your browser, register an account, and start posting. To try following, create a second account in a private/incognito window.

Optional: create an admin account with `python manage.py createsuperuser` and visit `/admin/`.

## API Overview

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/register/`, `/api/login/`, `/api/logout/` | Authentication |
| GET, POST | `/api/posts/` | List feed (`?scope=following` or `all`) and create a post |
| DELETE | `/api/posts/<id>/` | Delete your own post |
| POST | `/api/posts/<id>/like/` | Toggle like |
| GET, POST | `/api/posts/<id>/comments/` | List and add comments |
| DELETE | `/api/comments/<id>/` | Delete your own comment |
| GET | `/api/users/<username>/` | Profile data |
| PUT | `/api/users/me/` | Update your bio |
| POST | `/api/users/<username>/follow/` | Toggle follow |
| GET | `/api/users/search/?q=` | Search users |

## Author

Built by Buddharajlm as a learning project.
