import os
from functools import wraps
from datetime import date

from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash)
from werkzeug.security import check_password_hash, generate_password_hash

from models import db, User, Volunteer, Club, Event, Assignment

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'vms_college_secret_key_2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volunteer_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated


def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('logged_in'):
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('index'))
            if session.get('role') != role:
                flash('You do not have permission to access that page.', 'error')
                return redirect(url_for(route_after_login()))
            return f(*args, **kwargs)
        return decorated
    return wrapper


admin_required = role_required('admin')
volunteer_required = role_required('volunteer')


@app.context_processor
def inject_current_user():
    user = None
    if session.get('user_id'):
        user = db.session.get(User, session['user_id'])
    return {'current_user': user}


def route_after_login():
    if session.get('role') == 'volunteer':
        return 'volunteer_dashboard'
    return 'dashboard'


def sign_user_in(user):
    session.clear()
    session['logged_in'] = True
    session['user_id'] = user.id
    session['username'] = user.username
    session['name'] = user.name
    session['role'] = user.role
    session['volunteer_id'] = user.volunteer_id

# ---------------------------------------------------------------------------
# Seed data (runs only when DB is empty)
# ---------------------------------------------------------------------------

def seed_data():
    if Volunteer.query.count() > 0:
        return

    # Clubs
    club1 = Club(
        name='Tech Club',
        description='A community for technology enthusiasts — coding, hardware hacking, and open-source contributions.',
        coordinator_name='Prof. Anita Sharma'
    )
    club2 = Club(
        name='Cultural Club',
        description='Celebrating arts, music, dance, drama, and the rich cultural tapestry of our campus.',
        coordinator_name='Prof. Rajesh Mehta'
    )
    db.session.add_all([club1, club2])
    db.session.flush()   # get IDs before commit

    # Events
    event1 = Event(
        name='Hackathon 2024',
        date=date(2024, 11, 15),
        description='A 24-hour coding marathon where teams compete to build innovative solutions.',
        location='Main Auditorium',
        club_id=club1.id
    )
    event2 = Event(
        name='Tech Talk Series',
        date=date(2024, 12, 5),
        description='Industry experts share insights on AI, cloud computing, and startup culture.',
        location='Seminar Hall A',
        club_id=club1.id
    )
    event3 = Event(
        name='Annual Cultural Fest',
        date=date(2024, 12, 20),
        description='A grand showcase of music, dance, theatre, and fine art performances.',
        location='Open Air Theatre',
        club_id=club2.id
    )
    db.session.add_all([event1, event2, event3])
    db.session.flush()

    # Volunteers
    v1 = Volunteer(
        name='Rahul Verma',
        email='rahul.verma@college.edu',
        phone='9876543210',
        department='Computer Science',
        year_of_study=2,
        skills='Python, Web Development, Git'
    )
    v2 = Volunteer(
        name='Priya Patel',
        email='priya.patel@college.edu',
        phone='9876543211',
        department='Information Technology',
        year_of_study=3,
        skills='UI Design, Canva, Photoshop'
    )
    v3 = Volunteer(
        name='Arjun Singh',
        email='arjun.singh@college.edu',
        phone='9876543212',
        department='Electronics Engineering',
        year_of_study=1,
        skills='Arduino, Soldering, Circuit Design'
    )
    v4 = Volunteer(
        name='Sneha Kulkarni',
        email='sneha.kulkarni@college.edu',
        phone='9876543213',
        department='Computer Science',
        year_of_study=4,
        skills='Leadership, Event Management, Public Speaking'
    )
    db.session.add_all([v1, v2, v3, v4])
    db.session.flush()

    # Assignments
    a1 = Assignment(volunteer_id=v1.id, event_id=event1.id, hours_logged=8.0, status='completed')
    a2 = Assignment(volunteer_id=v4.id, event_id=event1.id, hours_logged=10.0, status='completed')
    a3 = Assignment(volunteer_id=v2.id, event_id=event3.id, hours_logged=5.0, status='pending')
    a4 = Assignment(volunteer_id=v3.id, event_id=event2.id, hours_logged=3.5, status='pending')
    db.session.add_all([a1, a2, a3, a4])

    db.session.commit()
    print('[VMS] Seed data inserted.')


def seed_default_admin():
    if User.query.filter_by(username='admin').first():
        return

    admin = User(
        name='Admin',
        username='admin',
        email='admin@volunteerhub.local',
        password_hash=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    print('[VMS] Default admin user created.')

# ---------------------------------------------------------------------------
# Routes — Auth
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for(route_after_login()))

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for(route_after_login()))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username, role='admin').first()
        if user and check_password_hash(user.password_hash, password):
            sign_user_in(user)
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid admin username or password. Please try again.', 'error')

    return render_template('index.html')


@app.route('/volunteer/login', methods=['GET', 'POST'])
def volunteer_login():
    if session.get('logged_in'):
        return redirect(url_for(route_after_login()))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username, role='volunteer').first()
        if user and check_password_hash(user.password_hash, password):
            sign_user_in(user)
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('volunteer_dashboard'))
        flash('Invalid volunteer username or password. Please try again.', 'error')

    return render_template('volunteer_login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('logged_in'):
        return redirect(url_for(route_after_login()))

    if request.method == 'POST':
        role = request.form.get('role', 'volunteer').strip()
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        department = request.form.get('department', '').strip()
        year_raw = request.form.get('year_of_study', '')

        if role not in ['admin', 'volunteer']:
            flash('Please choose a valid role.', 'error')
            return render_template('signup.html')
        if not name or not username or not email or not password:
            flash('Name, username, email, and password are required.', 'error')
            return render_template('signup.html')
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')
        if User.query.filter_by(username=username).first():
            flash('That username is already taken.', 'error')
            return render_template('signup.html')
        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'error')
            return render_template('signup.html')

        volunteer = None
        if role == 'volunteer':
            volunteer = Volunteer.query.filter_by(email=email).first()
            if not volunteer:
                volunteer = Volunteer(
                    name=name,
                    email=email,
                    department=department,
                    year_of_study=int(year_raw) if year_raw else 1,
                    skills=''
                )
                db.session.add(volunteer)
                db.session.flush()

        user = User(
            name=name,
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            volunteer_id=volunteer.id if volunteer else None
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully. Please sign in.', 'success')
        return redirect(url_for('volunteer_login' if role == 'volunteer' else 'login'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

# ---------------------------------------------------------------------------
# Routes — Dashboard
# ---------------------------------------------------------------------------

@app.route('/dashboard')
@admin_required
def dashboard():
    total_volunteers  = Volunteer.query.count()
    total_clubs       = Club.query.count()
    total_events      = Event.query.count()
    total_assignments = Assignment.query.count()

    recent_events     = Event.query.order_by(Event.id.desc()).limit(5).all()
    recent_volunteers = Volunteer.query.order_by(Volunteer.id.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        total_volunteers=total_volunteers,
        total_clubs=total_clubs,
        total_events=total_events,
        total_assignments=total_assignments,
        recent_events=recent_events,
        recent_volunteers=recent_volunteers
    )


@app.route('/volunteer/dashboard')
@volunteer_required
def volunteer_dashboard():
    volunteer = None
    assignments = []
    if session.get('volunteer_id'):
        volunteer = db.session.get(Volunteer, session['volunteer_id'])
        if volunteer:
            assignments = (
                Assignment.query
                .filter_by(volunteer_id=volunteer.id)
                .join(Event)
                .order_by(Event.date.desc())
                .all()
            )

    completed_count = sum(1 for assignment in assignments if assignment.status == 'completed')
    total_hours = sum(assignment.hours_logged or 0 for assignment in assignments)

    return render_template(
        'volunteer_dashboard.html',
        volunteer=volunteer,
        assignments=assignments,
        completed_count=completed_count,
        total_hours=total_hours
    )

# ---------------------------------------------------------------------------
# Routes — Volunteers
# ---------------------------------------------------------------------------

@app.route('/volunteers')
@admin_required
def volunteers():
    all_volunteers = Volunteer.query.order_by(Volunteer.id.asc()).all()
    return render_template('volunteers.html', volunteers=all_volunteers)


@app.route('/volunteers/add', methods=['GET', 'POST'])
@admin_required
def add_volunteer():
    if request.method == 'POST':
        name         = request.form.get('name', '').strip()
        email        = request.form.get('email', '').strip()
        phone        = request.form.get('phone', '').strip()
        department   = request.form.get('department', '').strip()
        year_raw     = request.form.get('year_of_study', '1')
        skills       = request.form.get('skills', '').strip()

        if not name or not email:
            flash('Name and Email are required.', 'error')
            return render_template('add_volunteer.html')

        if Volunteer.query.filter_by(email=email).first():
            flash('A volunteer with this email already exists.', 'error')
            return render_template('add_volunteer.html')

        volunteer = Volunteer(
            name=name,
            email=email,
            phone=phone,
            department=department,
            year_of_study=int(year_raw),
            skills=skills
        )
        db.session.add(volunteer)
        db.session.commit()
        flash(f'Volunteer "{name}" registered successfully!', 'success')
        return redirect(url_for('volunteers'))

    return render_template('add_volunteer.html')


@app.route('/volunteers/delete/<int:vid>')
@admin_required
def delete_volunteer(vid):
    volunteer = Volunteer.query.get_or_404(vid)
    name = volunteer.name
    db.session.delete(volunteer)
    db.session.commit()
    flash(f'Volunteer "{name}" has been removed.', 'success')
    return redirect(url_for('volunteers'))

# ---------------------------------------------------------------------------
# Routes — Clubs
# ---------------------------------------------------------------------------

@app.route('/clubs')
@admin_required
def clubs():
    all_clubs = Club.query.order_by(Club.id.asc()).all()
    return render_template('clubs.html', clubs=all_clubs)


@app.route('/clubs/add', methods=['GET', 'POST'])
@admin_required
def add_club():
    if request.method == 'POST':
        name             = request.form.get('name', '').strip()
        description      = request.form.get('description', '').strip()
        coordinator_name = request.form.get('coordinator_name', '').strip()

        if not name:
            flash('Club name is required.', 'error')
            return render_template('add_club.html')

        club = Club(name=name, description=description, coordinator_name=coordinator_name)
        db.session.add(club)
        db.session.commit()
        flash(f'Club "{name}" added successfully!', 'success')
        return redirect(url_for('clubs'))

    return render_template('add_club.html')


@app.route('/clubs/delete/<int:cid>')
@admin_required
def delete_club(cid):
    club = Club.query.get_or_404(cid)
    name = club.name
    db.session.delete(club)
    db.session.commit()
    flash(f'Club "{name}" and all its events have been removed.', 'success')
    return redirect(url_for('clubs'))

# ---------------------------------------------------------------------------
# Routes — Events
# ---------------------------------------------------------------------------

@app.route('/events')
@admin_required
def events():
    all_events = Event.query.order_by(Event.date.desc()).all()
    return render_template('events.html', events=all_events)


@app.route('/events/add', methods=['GET', 'POST'])
@admin_required
def add_event():
    all_clubs = Club.query.order_by(Club.name.asc()).all()

    if request.method == 'POST':
        name        = request.form.get('name', '').strip()
        date_str    = request.form.get('date', '')
        description = request.form.get('description', '').strip()
        location    = request.form.get('location', '').strip()
        club_id     = request.form.get('club_id', '')

        if not name or not date_str or not club_id:
            flash('Event name, date, and club are required.', 'error')
            return render_template('add_event.html', clubs=all_clubs)

        event = Event(
            name=name,
            date=date.fromisoformat(date_str),
            description=description,
            location=location,
            club_id=int(club_id)
        )
        db.session.add(event)
        db.session.commit()
        flash(f'Event "{name}" added successfully!', 'success')
        return redirect(url_for('events'))

    return render_template('add_event.html', clubs=all_clubs)


@app.route('/events/delete/<int:eid>')
@admin_required
def delete_event(eid):
    event = Event.query.get_or_404(eid)
    name = event.name
    db.session.delete(event)
    db.session.commit()
    flash(f'Event "{name}" has been removed.', 'success')
    return redirect(url_for('events'))

# ---------------------------------------------------------------------------
# Routes — Assignments
# ---------------------------------------------------------------------------

@app.route('/assign', methods=['GET', 'POST'])
@admin_required
def assign():
    all_volunteers = Volunteer.query.order_by(Volunteer.name.asc()).all()
    all_events     = Event.query.order_by(Event.date.desc()).all()

    if request.method == 'POST':
        volunteer_id = request.form.get('volunteer_id', '')
        event_id     = request.form.get('event_id', '')
        hours_raw    = request.form.get('hours_logged', '0')
        status       = request.form.get('status', 'pending')

        if not volunteer_id or not event_id:
            flash('Please select both a volunteer and an event.', 'error')
        else:
            assignment = Assignment(
                volunteer_id=int(volunteer_id),
                event_id=int(event_id),
                hours_logged=float(hours_raw) if hours_raw else 0.0,
                status=status
            )
            db.session.add(assignment)
            db.session.commit()
            flash('Volunteer assigned successfully!', 'success')
            return redirect(url_for('assign'))

    all_assignments = (
        Assignment.query
        .join(Volunteer).join(Event)
        .order_by(Assignment.id.desc())
        .all()
    )

    return render_template(
        'assign.html',
        volunteers=all_volunteers,
        events=all_events,
        assignments=all_assignments
    )


@app.route('/assign/delete/<int:aid>')
@admin_required
def delete_assignment(aid):
    assignment = Assignment.query.get_or_404(aid)
    db.session.delete(assignment)
    db.session.commit()
    flash('Assignment removed.', 'success')
    return redirect(url_for('assign'))

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
        seed_default_admin()
    app.run(debug=True)
