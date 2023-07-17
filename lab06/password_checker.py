import re
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userTable.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False) 



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


failed_attempts=0
@app.route('/report', methods=['POST'])
def report():
    global failed_attempts

    username = request.form['username']
    password = request.form['password']

    # Validate password using regex
    contains_uppercase, contains_lowercase, ends_with_number, password_size_check = validate_password(password)

    password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d.*\d$).{8,}$')
    passed_requirements = bool(password_pattern.match(password))

    if passed_requirements:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
    else:
        failed_attempts += 1

    warning = failed_attempts > 3

    return render_template('report.html', passed_requirements=passed_requirements,
                           contains_uppercase=contains_uppercase, contains_lowercase=contains_lowercase,
                           ends_with_number=ends_with_number, password_size_check=password_size_check,
                           warning=warning)



def validate_password(password):
    contains_uppercase = any(char.isupper() for char in password)
    contains_lowercase = any(char.islower() for char in password)
    ends_with_number = password[-1].isdigit()
    password_size_check = len(password) >= 8

    return contains_uppercase, contains_lowercase, ends_with_number, password_size_check


@app.route('/displayData', methods=['GET'])
def show_userdata():
    users = User.query.all()

    users_data = []

    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'password': user.password
        }
        users_data.append(user_data)

    return jsonify(users_data)

 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    
