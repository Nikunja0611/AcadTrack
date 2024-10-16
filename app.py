from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Student
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Load dataset and populate the database
def init_db():
    with app.app_context():
        db.create_all()
        if User.query.first() is None:
            df = pd.read_csv('data/students.csv')
            for index, row in df.iterrows():
                if row['role'] == 'student':
                    student = Student(
                        id=row['id'],
                        username=row['username'],
                        password=row['password'],
                        name=row['name'],
                        unit_test=row['unit_test'],
                        end_sem=row['end_sem'],
                        lab_attendance=row['lab_attendance'],
                        overall_attendance=row['overall_attendance']
                    )
                    db.session.add(student)
                elif row['role'] == 'professor':
                    prof = User(
                        id=row['id'],
                        username=row['username'],
                        password=row['password'],
                        role=row['role'],
                        name=row['name']
                    )
                    db.session.add(prof)
            db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            flash('Logged in successfully.')
            if user.role == 'professor':
                return redirect(url_for('professor_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        return redirect(url_for('professor_dashboard'))
    student = Student.query.filter_by(id=current_user.id).first()
    return render_template('dashboard.html', student=student)

@app.route('/profile')
@login_required
def profile():
    if current_user.role != 'student':
        return redirect(url_for('professor_dashboard'))
    student = Student.query.filter_by(id=current_user.id).first()
    return render_template('profile.html', student=student)

@app.route('/professor_dashboard')
@login_required
def professor_dashboard():
    if current_user.role != 'professor':
        return redirect(url_for('dashboard'))
    students = Student.query.all()
    # Calculate average marks
    avg_unit_test = db.session.query(db.func.avg(Student.unit_test)).scalar()
    avg_end_sem = db.session.query(db.func.avg(Student.end_sem)).scalar()
    avg_overall_attendance = db.session.query(db.func.avg(Student.overall_attendance)).scalar()
    
    above_avg = Student.query.filter(
        (Student.unit_test > avg_unit_test) &
        (Student.end_sem > avg_end_sem) &
        (Student.overall_attendance > avg_overall_attendance)
    ).all()
    
    avg_students = Student.query.filter(
        (Student.unit_test == avg_unit_test) &
        (Student.end_sem == avg_end_sem) &
        (Student.overall_attendance == avg_overall_attendance)
    ).all()
    
    below_avg = Student.query.filter(
        (Student.unit_test < avg_unit_test) |
        (Student.end_sem < avg_end_sem) |
        (Student.overall_attendance < avg_overall_attendance)
    ).all()
    
    defaulters = Student.query.filter(Student.overall_attendance < 60).all()
    
    return render_template('professor_dashboard.html',
                           students=students,
                           above_avg=above_avg,
                           avg_students=avg_students,
                           below_avg=below_avg,
                           defaulters=defaulters,
                           avg_unit_test=round(avg_unit_test,2),
                           avg_end_sem=round(avg_end_sem,2),
                           avg_overall_attendance=round(avg_overall_attendance,2))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
