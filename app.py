from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secretkey"  # Required for flash messages

# Temporary storage
users = []  # list of registered users
event_registrations = []  # list of event registrations

# Sample events
events_list = [
    {"id": 1, "name": "Tech Talk", "date": "2025-10-15"},
    {"id": 2, "name": "Workshop on AI", "date": "2025-10-20"},
    {"id": 3, "name": "Hackathon", "date": "2025-10-25"}
]
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # simple temporary login check
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        if user:
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for('events'))
        else:
            flash("Invalid credentials!", "danger")
            return redirect(url_for('login'))

    return render_template('login.html', title="Login")

# Home page
@app.route('/')
def home():
    return render_template('index.html', title="Home")

# User registration/login page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for('register'))

        # store user temporarily
        users.append({
            "username": username,
            "email": email,
            "password": password
        })
        flash(f"User {username} registered successfully!", "success")
        return redirect(url_for('login'))

    return render_template('event_register.html', title="Register")

# Events page
@app.route('/events')
def events():
    return render_template('events.html', title="Events", events=events_list)

# Event registration handling (POST only)
@app.route('/event_register', methods=['GET', 'POST'])
def event_register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        event_name = request.form.get('event_name')

        # check for missing fields
        if not username or not email or not event_name:
            flash("All fields are required!", "danger")
            return redirect(url_for('event_register'))

        # store event registration
        events_registrations.append({
            "username": username,
            "email": email,
            "event_name": event_name
        })
        flash(f"{username} successfully registered for {event_name}!", "success")
        return redirect(url_for('events'))

    return render_template('event_register.html')

# Contact page (optional)
@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Us")
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    # store user in temporary list
    users.append({"username": username, "email": email, "password": password})
    flash(f"{username} registered successfully!", "success")
    return redirect(url_for('events'))



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
