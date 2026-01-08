from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# -------------------
# App Configuration
# -------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'interia_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------
# Database Models
# -------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Designer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    specialty = db.Column(db.String(100))

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    designer_id = db.Column(db.Integer, db.ForeignKey('designer.id'))
    designer = db.relationship('Designer', backref='quotes')

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------
# Utility Function
# -------------------
def log_activity(message):
    log = ActivityLog(action=message)
    db.session.add(log)
    db.session.commit()

# -------------------
# Public Pages
# -------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('All fields are required')
            return redirect(url_for('signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('signup'))

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        log_activity(f"New customer registered: {email}")
        flash('Signup successful. Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')

# -------------------
# SINGLE LOGIN (ADMIN + CUSTOMER)
# -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('email_or_username', '').strip().lower()
        password = request.form.get('password', '').strip()

        # ADMIN LOGIN
        if identifier == 'admin' and password == 'password123':
            session.clear()
            session['admin_logged_in'] = True
            log_activity("Admin logged in")
            return redirect(url_for('admin_dashboard'))

        # CUSTOMER LOGIN
        user = User.query.filter_by(email=identifier).first()
        if user and user.password == password:
            session.clear()
            session['user_logged_in'] = True
            session['user_email'] = user.email
            log_activity(f"Customer logged in: {user.email}")
            return redirect(url_for('home'))

        flash('Invalid login credentials')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -------------------
# Other Pages
# -------------------
@app.route('/book')
def book():
    return render_template('book.html')



@app.route('/design')
def design():
    return render_template('design.html')

@app.route('/how')
def how():
    return render_template('how.html')

@app.route('/visit')
def visit():
    return render_template('visit.html')

@app.route('/show')
def show():
    return render_template('show.html')

# -------------------
# Submit Quote
# -------------------
@app.route('/submit_quote', methods=['POST'])
def submit_quote():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))

    quote = Quote(
        customer_name=request.form['name'],
        email=request.form['email'],
        mobile=request.form['mobile'],
        service=request.form['service']
    )
    db.session.add(quote)
    db.session.commit()

    log_activity(f"Quote submitted by {quote.email}")
    flash('Quote submitted successfully!')
    return redirect(url_for('book'))

# -------------------
# ADMIN DASHBOARD
# -------------------
@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    return render_template(
        'admin_dashboard.html',
        quotes=Quote.query.all(),
        designers=Designer.query.all(),
        users=User.query.all(),
        logs=ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(30)
    )

# -------------------
# Assign Designer
# -------------------
@app.route('/assign_designer/<int:quote_id>', methods=['POST'])
def assign_designer(quote_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    quote = Quote.query.get_or_404(quote_id)
    quote.designer_id = request.form['designer_id']
    quote.status = 'Assigned'
    db.session.commit()

    log_activity(f"Designer assigned to Quote #{quote.id}")
    return redirect(url_for('admin_dashboard'))

# -------------------
# Add Designer
# -------------------
@app.route('/add_designer', methods=['POST'])
def add_designer():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    designer = Designer(
        name=request.form['name'],
        email=request.form['email'],
        mobile=request.form['mobile'],
        specialty=request.form['specialty']
    )
    db.session.add(designer)
    db.session.commit()

    log_activity(f"Designer added: {designer.name}")
    return redirect(url_for('admin_dashboard'))

# -------------------
# Delete Customer
# -------------------
@app.route('/admin/delete-customer/<int:user_id>', methods=['POST'])
def delete_customer(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    log_activity(f"Customer deleted: {user.email}")
    return redirect(url_for('admin_dashboard'))

# -------------------
# Delete Designer
# -------------------
@app.route('/admin/delete-designer/<int:designer_id>', methods=['POST'])
def delete_designer(designer_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    designer = Designer.query.get_or_404(designer_id)
    db.session.delete(designer)
    db.session.commit()

    log_activity(f"Designer deleted: {designer.name}")
    return redirect(url_for('admin_dashboard'))

# -------------------
# Delete Quote
# -------------------
@app.route('/admin/delete-quote/<int:quote_id>', methods=['POST'])
def delete_quote(quote_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()

    log_activity(f"Quote deleted: #{quote_id}")
    return redirect(url_for('admin_dashboard'))

# -------------------
# Track Quote
# -------------------
@app.route('/track', methods=['GET', 'POST'])
def track_quote():
    quote = None
    if request.method == 'POST':
        quote = Quote.query.filter_by(mobile=request.form['mobile']).first()
    return render_template('track_quote.html', quote=quote)

# -------------------
# Run App
# -------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
