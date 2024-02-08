from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

instance_path = os.path.join(app.root_path, 'instance')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not os.path.exists(instance_path):
    os.makedirs(instance_path)

db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    coins = db.Column(db.Integer, default=0, nullable=False)
    donations = db.relationship('Donation', backref='user', lazy=True)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waste_type = db.Column(db.String(50))
    weight = db.Column(db.Float)
    state = db.Column(db.String(50))
    district = db.Column(db.String(50))
    username = db.Column(db.String(10), db.ForeignKey('user.username'))
    date = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    username = session.get('username')
    name = session.get('name')
    user = User.query.filter_by(username=username).first()
    if user:
        coins = user.coins
    else:
        coins = None
    return render_template('home.html', name=name,username=username, coins = coins)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            error = 'Username already exists. Please choose a different username.'
            return render_template('registration.html', error=error)

        new_user = User(username=username, name=name, email=email, password=password, coins=0)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = username
        session['name'] = name
        return redirect(url_for('home'))

    return render_template('registration.html')
1


def authenticate_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.name
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            if user.password == password:
                session['username'] = username
                name = authenticate_user(username)
                if name is not None:
                    session['name'] = name
                return redirect(url_for('home'))
            else:
                error = "Invalid password. Please try again."
        else:
            error = "Username is not registered with us. Please try again."

    return render_template('login.html', error=error)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = "Passwords do not match. Please try again."
            return render_template('forgot_password.html', error=error)

        user = User.query.filter_by(username=username).first()

        if user:
            user.password = password
            db.session.commit()
            return redirect(url_for('login'))
        else:
            error = "User not found. Please try again."
            return render_template('forgot_password.html', error=error)

    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


hubs_data = {
    'Andhra Pradesh': {
        'Visakhapatnam': ['Seethammadhara', 'Duvvada', 'MVP colony'],
        'Vizianagaram': ['Hub 4', 'Hub 5']
        
    },
    'Arunachal Pradesh': {
        'district3': ['Hub 6', 'Hub 7'],
        'district4': ['Hub 8', 'Hub 9', 'Hub 10']
    }
}

@app.route('/waste', methods=['GET', 'POST'])
def waste_type():
    if request.method == 'POST':
        waste_type = request.form['waste_type']
        return render_template('enter_weight.html', waste_type=waste_type)
    else:
        return render_template('waste_types.html')

@app.route('/weight', methods=['POST'])
def enter_weight():
    waste_type = request.form['waste_type']
    weight = request.form['weight']
    return render_template('address.html', waste_type=waste_type, weight=weight)

@app.route('/address', methods=['POST'])
def address():
    waste_type = request.form['waste_type']
    weight = request.form['weight']
    state = request.form['state']
    district = request.form['district']
    if not weight:
        flash('Weight is required.', 'error')
        return redirect(url_for('enter_weight'))

    try:
        weight = float(weight)
    except ValueError:
        flash('Invalid weight value.', 'error')
        return redirect(url_for('enter_weight'))

    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        hubs = hubs_data.get(state, {}).get(district, [])
        return render_template('hubs.html', hubs=hubs, state=state, district=district, waste_type=waste_type, weight=weight)

    return redirect(url_for('home'))

@app.route('/view_hubs', methods=['GET', 'POST'])
def view_hubs():
    if request.method == 'POST':
        state = request.form['state']
        district = request.form['district']
        hubs = hubs_data.get(state, {}).get(district, [])
        return render_template('hubs.html', hubs=hubs, state=state, district=district)
    else:
        state = request.args.get('state')
        district = request.args.get('district')
        hubs = hubs_data.get(state, {}).get(district, [])
        return render_template('hubs.html', hubs=hubs, state=state, district=district)



@app.route('/submit_donation', methods=['POST'])
def submit_donation():
    waste_type = request.form['waste_type']
    weight = request.form['weight']
    state = request.form['state']
    district = request.form['district']
    username = session.get('username')
    if weight:
        try:
            weight = float(weight)
        except ValueError:
            return redirect(url_for('home'))
    user = User.query.filter_by(username=username).first()
    if user:
        new_donation = Donation(waste_type=waste_type, weight=weight, state=state, district=district, username=username, date=datetime.utcnow())
        db.session.add(new_donation)
        db.session.commit()
        return render_template('thank_you.html')
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.gender = request.form['gender']
        db.session.commit()
        session['name'] = user.name
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=user)


@app.route('/logs')
def logs():
    donations = Donation.query.all()
    logs = []
    for donation in donations:
        if donation.date:
            date_string = donation.date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_string = '' 
        log = {
            'date': date_string,
            'action': 'Donation',
            'description': f"{donation.weight} kg of {donation.waste_type} donated in {donation.state}, {donation.district} Hub"
        }
        logs.append(log)
    return render_template('logs.html', logs=logs)


@app.route('/redeem', methods=['GET', 'POST'])
def redeem():
    return render_template('redeem.html')

if __name__ == '__main__':
    app.run()