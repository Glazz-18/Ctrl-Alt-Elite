from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
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
            stipend REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()
@app.route('/')
def index():
    return render_template('index.html')

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

        # Save to database
        conn = sqlite3.connect('internships.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO internships (intern_name, company_name, start_date, mentor_name, mentor_email, city, stipend)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (intern_name, company_name, start_date, mentor_name, mentor_email, city, stipend))
        conn.commit()
        conn.close()

        return redirect(url_for('view_internships'))

    return render_template('add_internship.html')

@app.route('/view_internships')
def view_internships():
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM internships')
    internships = cursor.fetchall()
    conn.close()

    return render_template('view_internships.html', internships=internships)

if __name__ == '__main__':
    app.run(debug=True)
