from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "qwertyuiop"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    complete = db.Column(db.Boolean())
    username = db.Column(db.String(100))


class Users(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    mail_id = db.Column(db.String(50))
    password = db.Column(db.String(50))


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=['POST'])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    query = db.session.query(Users).filter(Users.username == username, Users.password == password)
    result = query.first()
    if result:
        session['username'] = username
        return redirect(url_for("home"))
    else:
        flash('wrong username or password!')
        return redirect(url_for("login"))


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/add_user", methods=['POST'])
def add_user():
    name = request.form.get("username")
    mail = request.form.get("mail_id")
    psw = request.form.get("password")
    new_user = Users(username=name, mail_id=mail, password=psw)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("login"))


@app.route("/home")
def home():
    if "username" in session:
        todo_list = Todo.query.filter_by(username=session["username"])
        return render_template("home.html", todo_list=todo_list)
    else:
        return redirect(url_for("login"))


@app.route("/create", methods=['POST'])
def create():
    if "username" in session:
        name = request.form.get("name")
        new_task = Todo(name=name, complete=False, username=session["username"])
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


'''def read():
    todo = Todo.query.all()
    return redirect(url_for("home"))'''


@app.route('/update/<int:id>')
def update(id):
    if "username" in session:
        todo = Todo.query.get(id)
        todo.complete = not todo.complete
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/delete/<int:id>')
def delete(id):
    if "username" in session:
        todo = Todo.query.get(id)
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()
