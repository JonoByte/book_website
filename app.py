import datetime
import sqlite3
import subprocess

from flask import Flask, redirect, render_template, request, url_for

mydatabase = sqlite3.connect("databas.db", check_same_thread=False)
cur = mydatabase.cursor()
app = Flask(__name__)
datesss = datetime.date.today()
nows = "2018-05-25"
temp = datesss + datetime.timedelta(days = 30)
temp2 = temp - datetime.date.today()
print("int version:", nows.split("-")[0])
print(temp2)
def create_users_table():
    conn = sqlite3.connect("databas.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL)")
    conn.commit()
    conn.close()


def create_user_books_table():
    conn = sqlite3.connect("databas.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user_books (id INTEGER PRIMARY KEY, username TEXT NOT NULL, book TEXT NOT NULL, amount INTEGER NOT NULL)")
    conn.commit()
    conn.close()


# Route for handling the login page logic
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cur.fetchone()

        if user:
            return redirect(url_for("user_page", username=username))
        elif username == "admin" and password == "admin":
            return redirect(url_for("admin"))
        else:
            error = "Invalid Credentials. Please try again."

    return render_template("login.html", error=error)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    mydatabase2 = sqlite3.connect("databas.db")
    cur2 = mydatabase2.cursor()
    if request.method == "POST":
        if "title" in request.form:
            t = str(request.form["title"])
            p = int(request.form["price"])
            q = f"INSERT INTO books (title, price) VALUES ('{t}', '{p}')"
            print(q)
            cur2.execute(q)
        if "book_id" in request.form:
            for book in request.form.getlist("book_id"):
                cur2.execute(f"DELETE FROM books WHERE ID = {book}")
        mydatabase2.commit()

    cur2.execute("SELECT * FROM user_books")
    user_borrowed_data = cur2.fetchall()
    cur2.execute("SELECT * FROM guest")
    guest_data = cur2.fetchall()
    cur2.execute("SELECT * FROM Books")
    data = cur2.fetchall()
    return render_template(
        "admin.html",
        output_data=data,
        guest_data=guest_data,
        user_borrowed_data=user_borrowed_data,
    )


# create a display above to display loaned books ------------ DONE
# remove hard-code and check value of amount before allowing to loan or not to loan
# in admin html display guest loaned books -------------- DONE
# different users --------------- DONE
# create a timer on loaned books and display timer for all other users until the book is taken back to the library
# set a date in which the book was loaned from the database and then set a timer on 30 days if 30 within 30 days its not returned request payment
# compare date from database and write days remaining in the html code so database dont take a lot of pressure

@app.route("/guest", methods=["GET", "POST"])
def guest():
    mydatabase2 = sqlite3.connect("databas.db")
    cur2 = mydatabase2.cursor()
    if request.method == "POST":
        if "Title" in request.form:
            for title in request.form.getlist("Title"):
                print(title)
                print(type(title))
                cur2.execute("INSERT INTO guest(book, amount) VALUES(?, ?)", (title, 1))
        if "Loans" in request.form:
            for loan in request.form.getlist("select_loan"):
                cur2.execute(f"DELETE FROM guest WHERE ID = {loan}")
        mydatabase2.commit()
    cur2.execute("SELECT * FROM Books")
    data = cur2.fetchall()
    cur2.execute("SELECT * FROM guest")
    data2 = cur2.fetchall()
    return render_template("guest.html", output_data=data, output_data2=data2)


@app.route("/run-script", methods=["POST"])
def run_script():
    subprocess.run(["python", "/Users/datahaxx/Documents/jonathan/databas.py"])
    return "script ran"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["new_username"]
        password = request.form["new_password"]

        # conn = sqlite3.connect("databas.db")
        # cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cur.fetchone() is None:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            mydatabase.commit()
            # mydatabase.close()
            return redirect(url_for("user_page", username=username))
        else:
            return render_template(
                "login.html",
                error="User already exists, please choose another username.",
            )
    return render_template("login.html")


@app.route("/user_page/<username>", methods=["GET", "POST"])
def user_page(username):
    mydatabase2 = sqlite3.connect("databas.db")
    cur2 = mydatabase2.cursor()
    if request.method == "POST":
        if "Title" in request.form:
            for title in request.form.getlist("Title"):
                cur2.execute(
                    f"INSERT INTO user_books(username, book, amount, timestamp) VALUES(?, ?, ?, '{temp}')",
                    (username, title, 1),
                )
        mydatabase2.commit()
    cur2.execute("SELECT * FROM Books")
    data = cur2.fetchall()
    cur2.execute("SELECT * FROM user_books WHERE username=?", (username,))
    data2 = cur2.fetchall()
    return render_template(
        "user_page.html", username=username, output_data=data, output_data2=data2
    )


if __name__ == "__main__":
    #create_users_table()
    #create_user_books_table()
    app.run(debug=True)
