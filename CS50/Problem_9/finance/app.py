import os
import datetime
import pytz
import math
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
    try:
        db.execute("CREATE TABLE owned_share (symbol TEXT NOT NULL, shares INTEGER NOT NULL);")
    except RuntimeError:
        pass
    table = db.execute("SELECT * FROM trade_history WHERE id = ?", session["user_id"])
    portfolio = {}
    current_price = {}
    for action in table:
        shares = action["trade_shares"]
        stock = action["trade_stock"]
        if action["trade_type"] == "buy":
            if stock in portfolio:
                portfolio[stock] += shares
            else:
                portfolio[stock] = shares
        else:
            if stock in portfolio:
                portfolio[stock] -= shares

            else:
                portfolio[stock] = -shares
    portfolio = {key: value for key, value in portfolio.items() if value != 0}
    print("Portfolio: ", portfolio)
    for stock in portfolio:
        current_price[stock] = lookup(stock)
    buy_power = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    user_name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    for s in portfolio:
        intable = db.execute("SELECT * FROM owned_share WHERE symbol = ?", s)
        if intable:
            db.execute("UPDATE owned_share SET shares = ? WHERE symbol = ?", portfolio[s], s)
        else:
            db.execute("INSERT INTO owned_share (symbol, shares) VALUES (?, ?)", s, portfolio[s])
    print("Current Price: ", current_price)
    return render_template("index.html", portfolio=portfolio, current_price=current_price, buy_power=buy_power[0]["cash"], user_name=user_name)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not lookup(symbol):
            return render_template("apology.html", top="ERROR", bottom="Stock symbol error!", error=True), 400
        shares = request.form.get("shares")
        try:
            shares_f = float(shares)
            shares_1 = int(f"{shares_f: .0f}")
            if (shares_1 - shares_f == 0) and shares_f > 0:
                pass
            else:
                return render_template("apology.html", top="ERROR", bottom="Invalid shares!1", error=True), 400
        except:
            return render_template("apology.html", top="ERROR", bottom="Invalid shares!2", error=True), 400

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        buy_power = rows[0]["cash"]
        stock_data = lookup(symbol)
        print("stock data: ", stock_data)
        if buy_power >= stock_data["price"] * shares_f:
            buy_power -= stock_data["price"] * shares_f
            db.execute("UPDATE users SET cash = ? WHERE id = ?", buy_power, session["user_id"])
            db.execute("INSERT INTO trade_history (id, trade_stock, trade_type, trade_shares, trade_price, trade_dates) VALUES (?, ?, ?, ?, ?, ?)",
                        session["user_id"], symbol.upper(), "buy", shares, stock_data["price"], datetime.datetime.now(pytz.timezone("US/Eastern")))
            flash("Successful aquisition!")
            print("type: ", type(stock_data["price"]))
            return redirect("/")
        else:
            return render_template("apology.html", top="ERROR", bottom="Cannot afford the number of shares at the current price!", error=True), 400

    else:
        return render_template("buy.html")


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    # Fetch trade history from the database
    trade_history = db.execute("SELECT * FROM trade_history WHERE id = ?", session["user_id"])

    # Pagination parameters
    page = request.args.get("page", 1, type=int)
    latest = request.args.get("latest", 1, type=int)
    per_page = 10
    total_trades = len(trade_history)
    total_pages = math.ceil(total_trades / per_page)
    print("latest: ", latest)
    # Sort trade history based on 'latest' parameter
    if latest == 1:
        trade_history = sorted(trade_history, key=lambda x: x["trade_dates"], reverse=True)
    else:
        trade_history = sorted(trade_history, key=lambda x: x["trade_dates"])
    # Calculate start and end indices for the current page
    start = (page - 1) * per_page
    end = start + per_page
    trades_on_page = trade_history[start:end]

    return render_template("history.html", trade_history=trades_on_page, page=page, total_pages=total_pages, latest=latest)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            print(rows[0])
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        """important shit"""
        # Redirect user to home page
        flash("Login success!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    try:
        db.execute("DROP TABLE owned_share;")
    except RuntimeError:
        pass
    # Redirect user to login form
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock_data = lookup(symbol)
        if stock_data:
            return render_template("quote.html", output=1, symbol=symbol.upper(), price=stock_data["price"])
        else:
            return render_template("apology.html", top="ERROR", bottom="Invalid ticker symbol!", error=True), 400
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password0 = request.form.get("password")
        password1 = request.form.get("confirmation")
        if not username or not password0 or not password1:
            return render_template("apology.html", top="ERROR", bottom="Please fill out all requests!", error=True), 400
        elif password0 != password1:
            return render_template("apology.html", top="ERROR", bottom="Unequaled password!", error=True), 400
        else:
            repeated = db.execute("SELECT * FROM users WHERE username = ?", username)
            if not repeated:
                user_hash = generate_password_hash(password0)
                db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, user_hash)
            else:
                return render_template("apology.html", top="ERROR", bottom="Repeated user name!", error=True), 400
        loginuser = db.execute("SELECT * FROM users WHERE username = (?)", username)
        print(loginuser)
        session["user_id"] = loginuser[0]["id"]
        flash("Register success!")
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        try:
            symbol = request.form.get("symbol")
            portfolio = db.execute("SELECT * FROM owned_share WHERE symbol = ?", symbol.upper())
            shares = int(request.form.get("shares"))
        except RuntimeError:
            return render_template("apology.html", top="ERROR", bottom="No stock to sell!", error=True), 400
        except ValueError:
            return render_template("apology.html", top="ERROR", bottom="Enter Share!", error=True), 400
        for sym_port in portfolio:
            print(sym_port["symbol"])
            print(sym_port["shares"])
            if sym_port["symbol"] == symbol.upper() and sym_port["shares"] >= shares:
                table = lookup(sym_port["symbol"])
                current_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
                cash_add = float(table["price"]) * shares
                cash = current_cash[0]["cash"] + cash_add
                portfolio[0]["shares"] -= shares
                db.execute("UPDATE owned_share SET shares = ? WHERE symbol = ?",
                           portfolio[0]["shares"], sym_port["symbol"])
                db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
                db.execute("INSERT INTO trade_history (id, trade_stock, trade_type, trade_shares, trade_price, trade_dates) VALUES (?, ?, ?, ?, ?, ?)",
                           session["user_id"], symbol.upper(), "sell", shares, table["price"], datetime.datetime.now(pytz.timezone("US/Eastern")))
                flash("Sell success!")
                return redirect("/")
        return render_template("apology.html", top="ERROR", bottom="No stock in Portfolio!", error=True), 400
    else:
        portfolio = db.execute("SELECT symbol FROM owned_share")
        return render_template("sell.html", portfolio=[stock["symbol"] for stock in portfolio])
