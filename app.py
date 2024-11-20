from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Set the upload folder for the offer letters
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def init_db():
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intern_name TEXT NOT NULL,
            company_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            mentor_name TEXT NOT NULL,
            mentor_email TEXT NOT NULL,
            city TEXT NOT NULL,
            stipend REAL,
            offer_letter TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/add_internship', methods=['GET', 'POST'])
def add_internship():
    if request.method == 'POST':
        intern_name = request.form['intern_name']
        company_name = request.form['company_name']
        start_date = request.form['start_date']
        mentor_name = request.form['mentor_name']
        mentor_email = request.form['mentor_email']
        city = request.form['city']
        stipend = request.form['stipend']

        if 'offer_letter' not in request.files:
            return redirect(request.url)
        file = request.files['offer_letter']
        if file.filename == '':
            return redirect(request.url)
        
        offer_letter_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(offer_letter_path)

        conn = sqlite3.connect('internships.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO internships (intern_name, company_name, start_date, mentor_name, mentor_email, city, stipend, offer_letter)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (intern_name, company_name, start_date, mentor_name, mentor_email, city, stipend, offer_letter_path))
        conn.commit()
        conn.close()

        return redirect(url_for('student_dashboard'))

    return render_template('add_internship.html')

@app.route('/view_internships')
def view_internships():
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM internships')
    internships = cursor.fetchall()
    conn.close()

    return render_template('view_internships.html', internships=internships)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/student-dashboard')
def student_dashboard():
    return render_template('Student_Dashboard.html')

@app.route('/faculty-dashboard')
def faculty_dashboard():
    return render_template('Faculty_Deshboard.html')

if __name__ == '__main__':
    app.run(debug=True)