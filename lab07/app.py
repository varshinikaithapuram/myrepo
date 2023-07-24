from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets , re
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userTable.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secrets.token_hex(16)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d.*\d$).{8,}$')
        passed_requirements = bool(password_pattern.match(password))
        
        user = User.query.filter_by(email=email).first()
        if user:
                flash('Email address is already registered!', 'error')
                return render_template('signup.html', email_in_use=True)
        if password != confirm_password:
                flash('Passwords do not match! Please try again', 'error')
                return render_template('signup.html', password_not_match=True)
        if passed_requirements:
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('thankyou'))
        else : 
            return render_template('signup.html',didnot_passed_requirements= True)

    return render_template('signup.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find the user in the database based on the provided email
        user = User.query.filter_by(email=email).first()

        if user is not None and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('secret'))
        else:
            flash('Invalid email or password!', 'error')

    return render_template('signin.html')

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(email=username).first()

        if user is not None and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('secret'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('signin.html')

@app.route('/secret')
def secret():
    user_id = session.get('user_id')
    if user_id is not None:
        return render_template('secretpage.html')
    else:
        return redirect(url_for('sign_in'))


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/displayData', methods=['GET'])
def show_userdata():
    users = User.query.all()

    users_data = []

    for user in users:
        user_data = {
            'id': user.id,
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'password': user.password
        }
        users_data.append(user_data)

    return jsonify(users_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)