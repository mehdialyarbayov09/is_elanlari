from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            category TEXT NOT NULL,
            job_type TEXT NOT NULL,
            description TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    search_query = request.args.get('q', '')
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if search_query:
        cursor.execute("SELECT * FROM jobs WHERE title LIKE ? OR company LIKE ? ORDER BY id DESC", 
                       ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
        
    jobs = cursor.fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs, search_query=search_query)

@app.route("/add", methods=["GET", "POST"])
def add_job():
    if request.method == "POST":
        title = request.form["title"]
        company = request.form["company"]
        location = request.form["location"]
        category = request.form["category"]
        job_type = request.form["job_type"]
        description = request.form["description"]
        contact = request.form["contact"]
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jobs (title, company, location, category, job_type, description, contact) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (title, company, location, category, job_type, description, contact))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
        
    return render_template("add_job.html")

@app.route("/delete/<int:id>", methods=["POST"])
def delete_job(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/job/<int:id>")
def job_detail(id):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (id,))
    job = cursor.fetchone()
    conn.close()
    
    if job is None:
        return "Elan tapılmadı", 404
        
    return render_template("job_detail.html", job=job)

if __name__ == '__main__':
    init_sqlite_db()
    app.run(debug=True)