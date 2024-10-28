# PixPals

PixPals is a simple social media platform inspired by Instagram, built using Flask for the backend. It allows users to create posts, like, and favor posts, and interact with others through comments. Users can manage their personal profile, view their own posts, and explore posts they’ve liked or favored.

## Features

- **User Authentication** : Login, registration, and logout.
- **Post Management** : Create, like, and favor posts.
- **Profile Management** : View and update personal information.
- **Responsive Design** : Frontend layout inspired by Instagram.
- **Commenting System** : Add comments to posts.
- **User Dashboard** : View user’s own posts, liked posts, and favored posts.

## Project Structure

```
PixPals/
│
├── app.py               # Application entry point
├── config.py            # Configuration settings for Flask and database
├── models.py            # SQLAlchemy models for database tables
├── requirements.txt     # Python dependencies
│
├── auth/                # Authentication blueprint
│   ├── __init__.py
│   └── routes.py
│
├── user/                # User-related features (profile, settings)
│   ├── __init__.py
│   └── routes.py
│
├── post/                # Post-related features (create, like, favor)
│   ├── __init__.py
│   └── routes.py
│
├── utils/               # Utility modules (forms, helper functions)
│   └── forms.py
│
├── templates/           # HTML templates for the frontend
│   ├── layout.html
│   ├── index.html
│   └── user/
│       └── profile.html
│
└── static/              # Static assets (CSS, JavaScript, images)
  ├── avatars/
  └── posts/
```

## Requirements

- Python 3.x
- Flask 2.x
- Flask-SQLAlchemy
- Flask-Login
- Bootstrap 5 (via CDN)
- Bootstrap Icons (via CDN)

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/your-repository-url/pixpals.git
cd pixpals
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up the database:

```bash
python init_db.py
```

## How to Run

Activate the virtual environment (if not already activated):

```bash
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

Run the application:

```bash
python app.py
```

Access the application: Open your browser and go to:

```
http://127.0.0.1:5000/
```
