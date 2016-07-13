from flask import render_template, request, redirect, session
from Flask_server.auxiliary import *
from Flask_server import app
from Flask_server.database import db, User


@app.route('/')
def root_page():
    return redirect("/login")


@app.route('/send', methods=["POST", "GET"])
def send():
    if session['user'] is None:
        return redirect("/login")
    if request.method == "GET":
        return render_template("send_template.html")
    query = request.form["query"]
    result = wolframQuery(query)
    return render_template("result_template.html", pods=result)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login_template.html", incorrect=False)
    else:
        username, password = str(request.form["username"]), str(request.form["password"])

        logged = (User.query.filter_by(username=username, password=password) != None)

        if logged:
            session['user'] = username

            data = strToDict(oneUserSelect(username, "data", User))
            print(data)
            data["ip"] = request.remote_addr
            dat = dictToStr(data)
            oneUserUpdate(username, dict(data=dat), User, db)
            return redirect("/main")
        session.pop(config["key"], 0)
        return render_template("login_template.html", incorrect=True)


@app.route("/data", methods=["GET"])
def data():
    username = session['user']
    if username is None:
        return redirect("/login")
    else:
        res = strToDict(oneUserSelect(username, "data", User))
        return render_template("data_template.html", name=res["name"], ip=res["ip"], username=username)


@app.route("/main", methods=["GET"])
def mainPage():
    if session['user'] is None:
        return redirect("/login")
    username = session['user']
    res = strToDict(oneUserSelect(username, "data", User))['name']
    return render_template("main.html", name=res)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register_template.html")
    else:
        result = {"passdiff": False, "logintaken": False, "invlogin": False}
        username, password, repeat, name = request.form['username'], request.form['password'], request.form['repeat'], \
                                           request.form['name']

        print(username, password, repeat, name)

        if oneUserSelect(username, "data", User):
            result["logintaken"] = True
        if str(password[0]) != str(repeat[0]):
            result["passdiff"] = True
        result["invlogin"] = checkUsername(username)

        if result["passdiff"] or result["logintaken"] or result["invlogin"]:
            return render_template("register_template.html", **result)
        data = {"name": name, "ip": str(request.remote_addr)}
        newUser = User(username, password, dictToStr(data))
        insertUser(newUser, db)
        session['user'] = username
        return redirect("/main")
