# VolunteerHub - Volunteer Management System

VolunteerHub is a Flask-based volunteer management system for managing volunteers, clubs, events, assignments, and basic role-based access.

## Features

- Admin login
- Volunteer login
- Signup for admin and volunteer accounts
- Separate volunteer dashboard
- Admin dashboard with system totals
- Volunteer management
- Club management
- Event management
- Volunteer assignment tracking
- Hours and assignment status tracking
- Responsive UI with Lucide icons

## Roles

The project currently supports two roles:

- Admin: Can manage volunteers, clubs, events, and assignments.
- Volunteer: Can log in separately and view their own dashboard and assignments.

For this basic version, no other role is required. Future versions can add roles such as club coordinator, event manager, or faculty supervisor.

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Jinja2 templates
- HTML, CSS, JavaScript
- Lucide icons
- Werkzeug password hashing

## Project Structure

```text
.
├── app.py
├── models.py
├── requirements.txt
├── README.md
├── PROJECT_DOCUMENTATION.md
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    ├── base.html
    ├── index.html
    ├── volunteer_login.html
    ├── signup.html
    ├── dashboard.html
    ├── volunteer_dashboard.html
    ├── volunteers.html
    ├── add_volunteer.html
    ├── clubs.html
    ├── add_club.html
    ├── events.html
    ├── add_event.html
    └── assign.html
```

The SQLite database is created automatically inside the `instance/` folder when the app runs.

## Installation

For a beginner-friendly download and setup guide, see `FRIEND_SETUP_GUIDE.md`.

### 1. Clone the repository

```bash
git clone https://github.com/Swastik-4752/VMS.git
cd VMS
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python app.py
```

Open the app in your browser:

```text
http://127.0.0.1:5000
```

## Default Admin Login

The app creates a default admin account automatically if it does not exist.

```text
Username: admin
Password: admin123
```

Admin login page:

```text
http://127.0.0.1:5000/login
```

Volunteer login page:

```text
http://127.0.0.1:5000/volunteer/login
```

Signup page:

```text
http://127.0.0.1:5000/signup
```

## Environment Variables

For local development, the app works without environment variables.

For a safer deployment, set a custom Flask secret key:

```bash
set SECRET_KEY=your-secret-key
```

On macOS or Linux:

```bash
export SECRET_KEY=your-secret-key
```

## Database

The project uses SQLite by default:

```text
instance/volunteer_db.sqlite
```

This file is ignored by Git because it is generated locally. To reset the database, stop the server, delete the SQLite file, and run the app again.

## Development Notes

- Main backend code is in `app.py`.
- Database models are in `models.py`.
- HTML templates are in `templates/`.
- CSS and JavaScript are in `static/`.
- Detailed development documentation is available in `PROJECT_DOCUMENTATION.md`.

## Verify Setup

After installing dependencies, you can check Python syntax with:

```bash
python -m compileall app.py models.py
```

Then run:

```bash
python app.py
```

If the server starts and `http://127.0.0.1:5000` opens, the setup is working.
