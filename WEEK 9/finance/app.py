import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    index = {}
    moc = db.execute("SELECT symbol, quantity FROM portfolio WHERE id = ?", session["user_id"])
    for row in moc:
        if row["symbol"] not in index:
            stock_info = lookup(row["symbol"])
            row["price"] = stock_info["price"]
            row["total"] = row["price"] * row["quantity"]
            index[row["symbol"]] = {"quantity": row["quantity"], "price": row["price"], "total": row["total"]}
        else:
            index[row["symbol"]]["quantity"] += row["quantity"]
            index[row["symbol"]]["total"] = index[row["symbol"]]["price"] * index[row["symbol"]]["quantity"]

    cos = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = float(cos[0]["cash"])

    #TOTAL
    total = cash
    for i in index:
        total += index[i]["price"] * index[i]["quantity"]


    total = usd(total)
    cash = usd(cash)

    for symbol in index:
        index[symbol]["price"] = usd(index[symbol]["price"])
        index[symbol]["total"] = usd(index[symbol]["total"])


    return render_template("index.html", index=index, cos=cos, moc=moc, total=total, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        #get the dictionairy of a symbol
        look = lookup(request.form.get("symbol"))
         #ensure check symbol is correct
        if look is None:
            return apology("Stock doesn't exist", 400)
        if not request.form.get("symbol"):
            return apology("You must provide stock symbol", 400)

        price = look["price"]
        symbol = look["symbol"]
        #get shares as a integer
        shares_s = request.form.get("shares")
        if not shares_s.isdigit() or int(shares_s) <= 0:
            return apology("Shares must be a positive integer", 400)

        shares = int(shares_s)

        #check available stock
        cos = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cos[0]["cash"]

        #check new saldo
        saldo = cash - (shares * price)

        #ensure stock number i correct
        if saldo < 0:
            return apology("You don't have enough money, my friend", 400)

        else:
            #reduce users cash
            db.execute("UPDATE users SET cash = ? WHERE id = ?", saldo, session["user_id"])

            #add stock to portfolio
            db.execute("INSERT INTO portfolio (id, symbol, quantity) VALUES (?, ?, ?)", session["user_id"], symbol, shares)
            index = {}
            moc = db.execute("SELECT symbol, quantity FROM portfolio WHERE id = ?", session["user_id"])
            for row in moc:
                if row["symbol"] not in index:
                    stock_info = lookup(row["symbol"])
                    row["price"] = stock_info["price"]
                    row["total"] = row["price"] * row["quantity"]
                    index[row["symbol"]] = {"quantity": row["quantity"], "price": row["price"], "total": row["total"]}
                else:
                    index[row["symbol"]]["quantity"] += row["quantity"]
                    index[row["symbol"]]["total"] = index[row["symbol"]]["price"] * index[row["symbol"]]["quantity"]

            cos = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            cash = float(cos[0]["cash"])

            # get the currecnt price of the share
            lookup_result = lookup(request.form.get("symbol"))
            if lookup_result is None:
                return apology("WRRRR", 400)
            price_per_share = lookup_result["price"]


            #add transaction data
            db.execute("INSERT INTO transactions (id, symbol, quantity, price, type) VALUES (?, ?, ?, ?, ?)", session["user_id"], request.form.get("symbol"), shares, price_per_share, "BOUGHT")


            #TOTAL
            total = cash
            for i in index:
                total += index[i]["price"] * index[i]["quantity"]


            total = usd(total)
            cash = usd(cash)

            for symbol in index:
                index[symbol]["price"] = usd(index[symbol]["price"])
                index[symbol]["total"] = usd(index[symbol]["total"])


            return render_template("bought.html",index=index, cos=cos, moc=moc, total=total, cash=cash)

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    pip = db.execute("SELECT * FROM transactions WHERE id = ?", session["user_id"])
    for row in pip:
        row['price'] = usd(row['price'])
    index = {}
    moc = db.execute("SELECT symbol, quantity FROM portfolio WHERE id = ?", session["user_id"])
    for row in moc:
        if row["symbol"] not in index:
            stock_info = lookup(row["symbol"])
            row["price"] = stock_info["price"]
            row["total"] = row["price"] * row["quantity"]
            index[row["symbol"]] = {"quantity": row["quantity"], "price": row["price"], "total": row["total"]}
        else:
            index[row["symbol"]]["quantity"] += row["quantity"]
            index[row["symbol"]]["total"] = index[row["symbol"]]["price"] * index[row["symbol"]]["quantity"]

    cos = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = float(cos[0]["cash"])

    #TOTAL
    total = cash
    for i in index:
        total += index[i]["price"] * index[i]["quantity"]


    total = usd(total)
    cash = usd(cash)

    return render_template("history.html", pip=pip, total=total, cash=cash)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        look = lookup(request.form.get("symbol"))
        if look is None:
            return apology("Stock symbol doesn't exist", 400)
        if not request.form.get("symbol"):
            return apology("EEEE", 400)

        else:
            ma = look["price"]
            ma = usd(ma)
            return render_template("lookup.html", look=look, ma=ma)


    else:
        return render_template("quote.html")


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



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    symbol = []
    check = db.execute("SELECT symbol from portfolio WHERE id = ?", session["user_id"] )
    if check is not None:
        for row in check:
            if row['symbol'] not in symbol:
                symbol.append(row['symbol'])

    if request.method == "POST":
        check2 = db.execute("SELECT symbol, quantity from portfolio WHERE id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))
        ilosc = {}

        if check2 is not None:
            for row in check2:
                if row['symbol'] not in ilosc:
                    ilosc[row['symbol']] = row['quantity']
                else:
                    ilosc[row['symbol']] += row['quantity']

        if not request.form.get("symbol"):
            return apology("You must select a symbol", 400)

        shares = request.form.get("shares")
        shares = int(shares)
        if shares <= 0:
            return apology("Must be more than 0", 400)

        for symbol, quantity in ilosc.items():
            if request.form.get("symbol") == symbol:
                if shares > quantity:
                    return apology("You don't have enough shares", 400)

        else:

            # get the currecnt price of the share
            lookup_result = lookup(request.form.get("symbol"))
            if lookup_result is None:
                return apology("WRRRR", 400)
            price_per_share = lookup_result["price"]

            #calculate the toal value of the sold shares
            total_value = price_per_share * shares

            #substracct the sold shares from the user's portfolio
            db.execute("UPDATE portfolio SET quantity = quantity - ? WHERE id = ? AND symbol = ?", shares, session["user_id"], request.form.get("symbol"))
            #add money
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_value, session["user_id"])

            #add transaction data
            db.execute("INSERT INTO transactions (id, symbol, quantity, price, type) VALUES (?, ?, ?, ?, ?)", session["user_id"], request.form.get("symbol"), shares, price_per_share, "SOLD")

            index = {}
            moc = db.execute("SELECT symbol, quantity FROM portfolio WHERE id = ?", session["user_id"])
            for row in moc:
                if row["symbol"] not in index:
                    stock_info = lookup(row["symbol"])
                    row["price"] = stock_info["price"]
                    row["total"] = row["price"] * row["quantity"]
                    index[row["symbol"]] = {"quantity": row["quantity"], "price": row["price"], "total": row["total"]}
                else:
                    index[row["symbol"]]["quantity"] += row["quantity"]
                    index[row["symbol"]]["total"] = index[row["symbol"]]["price"] * index[row["symbol"]]["quantity"]

            cos = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            cash = float(cos[0]["cash"])

            #TOTAL
            total = cash
            for i in index:
                total += index[i]["price"] * index[i]["quantity"]


            total = usd(total)
            cash = usd(cash)

            for symbol in index:
                index[symbol]["price"] = usd(index[symbol]["price"])
                index[symbol]["total"] = usd(index[symbol]["total"])


            return render_template("sold.html", index=index, cos=cos, moc=moc, total=total, cash=cash)

    else:
        return render_template("sell.html", symbol=symbol)

@app.route("/cheater", methods=["GET", "POST"])
@login_required
def cheater():
    """Sell shares of stock"""

    if request.method == "POST":
        value = request.form.get("value")
        if not request.form.get("value"):
            return apology("Don't be shy :}", 400)
        if not request.form.get("value").isdigit():
            return apology("Only numbers, my friend :|", 400)

        else:
            value = int(value)
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", value, session["user_id"])

        return render_template("cheated.html")



    return render_template("cheater.html")