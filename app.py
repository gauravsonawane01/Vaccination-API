from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, AppointmentForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL

from auth import auth, APIKEY
from flask import Flask, render_template, request
from states import states

from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gaurav.sonawane@cuelogic.com'
app.config['MAIL_PASSWORD'] = 'gauravps4'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/testapi'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(id))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    appointment = db.relationship('Appointment', backref='user', uselist=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phoneNumber = db.Column(db.BigInteger, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'phoneNumber': self.phoneNumber,
            'age': self.age,
            'date': self.date,
            'city': self.city,
            'state': self.state,
            'zip': self.zip
        }
'''
class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'))
    appointment_age = db.Column(db.Integer, db.ForeignKey('appointment.age'))
    appointment_date = db.Column(db.String(20), db.ForeignKey('appointment.date'))
    appointment_city = db.Column(db.String(20), db.ForeignKey('appointment.city'))
    appointment_state = db.Column(db.String(20), db.ForeignKey('appointment.state'))
    appointment_zip = db.Column(db.Integer, db.ForeignKey('appointment.zip'))

    def to_dict(self):
        return {
            'fname': self.user_fname,
            'lname': self.user_lname,
            'age' : self.age,
            'date': self.date,
            'city': self.city,
            'state': self.state,
            'zip': self.zip
        }
'''

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', title='dashboard')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():


        #hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(fname=form.fname.data, lname=form.lname.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if (user.password == form.password.data):
                #login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))


        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

#Book Appointment
@app.route("/appointment", methods=['GET', 'POST'])
def appoint():
    form = AppointmentForm()

    if form.validate_on_submit():
        email = request.form['email']

        msg = Message('Confirm Booking', sender='gaurav.sonawane@cuelogic.com', recipients=[email])

        msg.body = 'Your Slot is Confirmed'

        mail.send(msg)
        new_appointment = Appointment(phoneNumber=form.phoneNumber.data, age=form.age.data, date=form.date.data, city=form.city.data, state=form.state.data, zip=form.zip.data )
        db.session.add(new_appointment)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('form.html', form=form)


mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'testapi'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/view")
def view():
    con = mysql.connect()
    #con.row_factory = mysql.Row
    cur = con.cursor()
    cur.execute(" select user.id, user.fname,user.lname,appointment.age,appointment.city, appointment.state from user inner join appointment where user.id=appointment.id")
    rows = cur.fetchall()
    cur.close()
    cur1 = con.cursor()
    cur1.execute("select * from Appointment")
    data = cur1.fetchall()
    cur1.close()

    return render_template("view2.html", rows = rows, data = data)

@app.route("/filter1845")
def filter1845():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute("select * from Appointment WHERE age>=18 and age<=45")
    rows = cur.fetchall()
    cur.close()
    return render_template("view2.html", rows=rows, data=data)

@app.route("/filter45")
def filter45():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute("select * from Appointment WHERE age>=45")
    rows = cur.fetchall()
    cur.close()
    return render_template("view2.html", rows=rows, data=data)

@app.route('/search')
def index():
    return render_template('ajax_table.html', title='USER LIST')


@app.route('/api/data')
def data():
    return {'data': [Appointment.to_dict() for Appointment in Appointment.query]}



if __name__ == '__main__':
    app.run(debug=True)