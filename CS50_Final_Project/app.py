import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import login_required, apology, get_countries, get_continents

# Save regions
countries = get_countries()
continents = get_continents()


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///zayerbani.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """ ??? """

    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
# User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))

        #Ensure password and confirmation match, else return an apology
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match", 400)

        #Ensure username is not already taken, else return an apology
        if len(rows) != 0:
            return apology("Username is already taken", 400)


        # Generate a hash of the password
        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha1', salt_length=8)
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), hash)

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/yerbamate", methods=["GET", "POST"])
@login_required
def yerbamate():

        #set dictionairy of producers
    producents = []
    get_producents = db.execute("SELECT producer FROM yerbas")
    for producent in get_producents:
        if producent not in producents:
            producents.append(producent)


    #set dictionairy of flavors
    flavors = []
    get_flavors = db.execute("SELECT flavor FROM yerbas")
    for x in get_flavors:
        if x not in flavors:
            flavors.append(x)
        if x in flavors:
                None

    if request.method == "POST":


        #get values from requests
        flavor = request.form.get("flavors")
        producer = request.form.get("producents")
        price = request.form.get("price")


        if not price:
            price = 999999
        else:
            price = int(price)

        if not flavor:
            if producer == "None":
                results = db.execute("SELECT * FROM yerbas JOIN yerbas_ratings ON yerbas.id = yerbas_ratings.yerba_id WHERE price < ?", price)
            else:
                results = db.execute("SELECT * FROM yerbas JOIN yerbas_ratings ON yerbas.id = yerbas_ratings.yerba_id WHERE producer = ? AND price < ?", producer, price)
            for result in results:
                user_rating = db.execute("SELECT rating FROM ratings WHERE user_id = ? AND yerba_id = ?", session["user_id"], result['yerba_id'])
                result['user_rating'] = user_rating[0]['rating'] if user_rating else None




        if not producer:
            if flavor == "None":
                results = db.execute("SELECT * FROM yerbas JOIN yerbas_ratings ON yerbas.id = yerbas_ratings.yerba_id WHERE price < ?", price)
            else:
                results = db.execute("SELECT * FROM yerbas JOIN yerbas_ratings ON yerbas.id = yerbas_ratings.yerba_id WHERE flavor = ? AND price < ?", flavor, price)
            for result in results:
                user_rating = db.execute("SELECT rating FROM ratings WHERE user_id = ? AND yerba_id = ?", session["user_id"], result['yerba_id'])
                result['user_rating'] = user_rating[0]['rating'] if user_rating else None



        return render_template("yerbamateresults.html", results=results, producer=producer, flavor=flavor, price=price, user_rating=user_rating)

    if request.method == "GET":

        return render_template("yerbamate.html", producents=producents, flavors=flavors)




@app.route("/rateme", methods=["GET", "POST"])
@login_required
def rateme():


    return render_template("rateme.html")

@app.route("/yerbamateresults", methods=["GET", "POST"])
def yerbamateresults():

    if request.method == "POST":


        ocena = int(request.form.get("rate"))
        yerba_id = request.form.get("yerba_id")
        #dodac komende, gdzie dodaje do tabeli yerba_ratings votes +1 i obliczam rating i wyswietlam
        db.execute("INSERT INTO ratings (user_id, yerba_id, rating) VALUES (?, ?, ?)", session["user_id"], yerba_id, ocena)
        db.execute("UPDATE yerbas_ratings SET votes = votes + 1, rating = ? WHERE yerba_id = ?", ocena, yerba_id)

        return redirect(url_for('yerbamate'))

    return render_template("yerbamatersults.html", products=products, user_ratings=user_ratings)


@app.route("/top", methods=["GET", "POST"])
def top():

    results = db.execute("SELECT * FROM yerbas JOIN yerbas_ratings ON yerbas.id = yerbas_ratings.yerba_id ORDER BY rating DESC LIMIT 5")

    return render_template("top.html", results=results)

@app.route("/history", methods=["GET", "POST"])
def history():

    results = db.execute("SELECT * FROM yerbas JOIN ratings ON yerbas.id = ratings.yerba_id WHERE user_id = ? ORDER BY date_rated DESC", session["user_id"])

    return render_template("history.html", results=results)