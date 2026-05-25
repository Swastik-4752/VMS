# VolunteerHub Project Documentation

This document explains the coding and development side of the VolunteerHub project. It focuses on the current implementation, file structure, database models, authentication system, routes, UI templates, and how to run or extend the project.

## 1. Technology Stack

The project is built as a simple Flask web application.

- Backend: Python with Flask
- Database: SQLite
- ORM: Flask-SQLAlchemy
- Templates: Jinja2 HTML templates
- Styling: Plain CSS
- JavaScript: Plain vanilla JavaScript
- Icons: Lucide icons through CDN
- Password security: Werkzeug password hashing

The project does not use a frontend framework like React or Vue. All pages are rendered from Flask templates.

## 2. Project Folder Structure

```text
Ajinath/
  app.py
  models.py
  PROJECT_DOCUMENTATION.md
  instance/
    volunteer_db.sqlite
  static/
    style.css
    script.js
  templates/
    base.html
    index.html
    volunteer_login.html
    signup.html
    dashboard.html
    volunteer_dashboard.html
    volunteers.html
    add_volunteer.html
    clubs.html
    add_club.html
    events.html
    add_event.html
    assign.html
```

## 3. Main Application File

The main application logic is inside `app.py`.

This file is responsible for:

- Creating the Flask app
- Configuring the SQLite database
- Initializing SQLAlchemy
- Creating authentication helpers
- Creating admin and volunteer routes
- Seeding demo data
- Running the development server

Important setup code:

```python
app = Flask(__name__)
app.secret_key = 'vms_college_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volunteer_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
```

The SQLite database is stored inside the `instance` folder as:

```text
instance/volunteer_db.sqlite
```

## 4. Database Models

The database models are defined in `models.py`.

### User Model

The `User` model handles login accounts.

Fields:

- `id`: Primary key
- `name`: Full name of the user
- `username`: Unique login username
- `email`: Unique email address
- `password_hash`: Hashed password
- `role`: User role, currently `admin` or `volunteer`
- `volunteer_id`: Optional link to a volunteer profile
- `created_at`: Account creation timestamp

This model is used for both admin and volunteer login.

### Volunteer Model

The `Volunteer` model stores volunteer profile data.

Fields:

- `id`
- `name`
- `email`
- `phone`
- `department`
- `year_of_study`
- `skills`

A volunteer can have many assignments.

### Club Model

The `Club` model stores club details.

Fields:

- `id`
- `name`
- `description`
- `coordinator_name`

A club can have many events.

### Event Model

The `Event` model stores event details.

Fields:

- `id`
- `name`
- `date`
- `description`
- `location`
- `club_id`

Each event belongs to one club.

### Assignment Model

The `Assignment` model connects volunteers to events.

Fields:

- `id`
- `volunteer_id`
- `event_id`
- `hours_logged`
- `status`

The status is currently either:

- `pending`
- `completed`

## 5. Authentication System

The project now has a basic working login and signup system.

There are two supported roles:

- Admin
- Volunteer

No extra roles are currently required for this basic project. In a bigger system, possible future roles could be:

- Club coordinator
- Event manager
- Faculty supervisor

For the current app, admin and volunteer are enough.

### Admin Login

Admin login page:

```text
/login
```

Default admin account:

```text
Username: admin
Password: admin123
```

The default admin account is created by `seed_default_admin()` if it does not already exist.

### Volunteer Login

Volunteer login page:

```text
/volunteer/login
```

Volunteer users can create an account from the signup page and then log in from the volunteer login page.

### Signup

Signup page:

```text
/signup
```

The signup form allows the user to choose:

- Volunteer account
- Admin account

When a volunteer signs up, the app also creates or links a volunteer profile using the same email address.

Passwords are not stored directly. They are stored as hashes using Werkzeug:

```python
generate_password_hash(password)
check_password_hash(user.password_hash, password)
```

## 6. Session Handling

After successful login, user information is stored in the Flask session.

Session values:

```python
session['logged_in']
session['user_id']
session['username']
session['name']
session['role']
session['volunteer_id']
```

These values are used to decide:

- Whether the user is logged in
- Which dashboard to show
- Whether the user has permission to access a route

## 7. Role Protection

The app uses decorators to protect routes.

### Login Required

Checks whether the user is logged in.

```python
@login_required
```

### Admin Required

Allows only admin users.

```python
@admin_required
```

Admin routes include:

- `/dashboard`
- `/volunteers`
- `/clubs`
- `/events`
- `/assign`

### Volunteer Required

Allows only volunteer users.

```python
@volunteer_required
```

Volunteer route:

```text
/volunteer/dashboard
```

## 8. Main Routes

### Public Routes

```text
/                  Redirects to login or dashboard
/login             Admin login
/volunteer/login   Volunteer login
/signup            Create new account
/logout            Logout current user
```

### Admin Routes

```text
/dashboard                 Admin dashboard
/volunteers                View volunteers
/volunteers/add            Add volunteer
/volunteers/delete/<id>    Delete volunteer
/clubs                     View clubs
/clubs/add                 Add club
/clubs/delete/<id>         Delete club
/events                    View events
/events/add                Add event
/events/delete/<id>        Delete event
/assign                    Assign volunteers to events
/assign/delete/<id>        Remove assignment
```

### Volunteer Routes

```text
/volunteer/dashboard       Volunteer dashboard
```

## 9. Templates

All HTML files are inside the `templates` folder.

### base.html

This is the main layout file.

It contains:

- HTML head
- CSS link
- Lucide icon script
- Navbar
- Flash message display
- Main content block
- JavaScript link

Other templates extend this file using:

```jinja2
{% extends 'base.html' %}
```

### index.html

Admin login page.

### volunteer_login.html

Volunteer login page.

### signup.html

Signup page for admin and volunteer accounts.

### dashboard.html

Admin dashboard showing:

- Total volunteers
- Total clubs
- Total events
- Total assignments
- Recent events
- Recent volunteers
- Quick action buttons

### volunteer_dashboard.html

Volunteer dashboard showing:

- Volunteer assignments
- Completed assignment count
- Logged hours
- Assignment status

### Management Templates

These templates are for admin management pages:

- `volunteers.html`
- `add_volunteer.html`
- `clubs.html`
- `add_club.html`
- `events.html`
- `add_event.html`
- `assign.html`

## 10. Static Files

Static files are inside the `static` folder.

### style.css

This file controls the complete UI design.

It includes styles for:

- Layout
- Navbar
- Buttons
- Login cards
- Signup form
- Tables
- Dashboard stat cards
- Forms
- Flash messages
- Responsive mobile layout

The UI uses a clean professional theme with Lucide icons instead of emoji icons.

### script.js

This file handles small frontend interactions.

Features:

- Delete confirmation
- Password show/hide toggle
- Flash message auto-dismiss
- Mobile navbar toggle
- Default event date behavior
- Table row focus support
- Signup role picker behavior
- Lucide icon initialization

## 11. Database Seeding

The app has two seed functions.

### seed_data()

Creates demo data when the volunteer table is empty.

Seed data includes:

- Clubs
- Events
- Volunteers
- Assignments

### seed_default_admin()

Creates the default admin account if it does not already exist.

```text
Username: admin
Password: admin123
```

## 12. How to Run the Project

Open a terminal in the project folder:

```powershell
cd C:\Users\banka\Desktop\Ajinath
```

Run the Flask app:

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

The app will create the database tables automatically if they do not exist.

## 13. Development Flow

A normal development flow for this project is:

1. Update models in `models.py`
2. Update routes in `app.py`
3. Update templates in `templates`
4. Update styling in `static/style.css`
5. Update interactions in `static/script.js`
6. Run the app using `python app.py`
7. Test admin and volunteer flows in the browser

## 14. Current Working Login Flow

### Admin

1. Go to `/login`
2. Enter admin credentials
3. App checks the `User` table for an admin user
4. Password is verified using password hash checking
5. Session is created
6. Admin is redirected to `/dashboard`

### Volunteer

1. Go to `/signup`
2. Create a volunteer account
3. App creates a `User` account
4. App creates or links a `Volunteer` profile
5. Volunteer logs in from `/volunteer/login`
6. Volunteer is redirected to `/volunteer/dashboard`

## 15. Current Permission Rules

Admin can:

- View dashboard
- Add volunteers
- Delete volunteers
- Add clubs
- Delete clubs
- Add events
- Delete events
- Assign volunteers to events
- Remove assignments

Volunteer can:

- Log in separately
- View own dashboard
- View own event assignments
- View hours and assignment status

Volunteer cannot:

- Access admin dashboard
- Manage clubs
- Manage events
- Delete data
- Assign volunteers

## 16. Notes for Future Development

Possible future improvements:

- Add edit pages for volunteers, clubs, events, and assignments
- Add profile editing for volunteers
- Add admin approval for new admin accounts
- Add forgot password flow
- Add stronger password rules
- Add pagination and search
- Add role for club coordinator
- Add event attendance marking
- Add reports for total hours by volunteer

For the current basic version, the implemented admin and volunteer role system is enough and works with the existing project structure.
