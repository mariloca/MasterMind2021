import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
import mainloop
import rand
#API_KEY=pk_b94486403d79464faadabbc3d003ec44
#message flashing
#https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/

# Configure application
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

'''
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
'''

'''
# Custom filter
app.jinja_env.filters["usd"] = usd
'''

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mastermind.db")

'''
# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
'''

secret=rand.randomnumbergenerate(4,0,7) #Generate random number in a list
print(secret)

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    score=100#request.form.get("score")

    print("score",score)
    #return render_template('index.html')
    if score!=0:
        if request.method == "GET":
            #flash(secret)
            return render_template("index.html")
        else:
            guess_1 = request.form.get("guess_1")

            # guess_2 = request.form.get("guess_2")
            if not guess_1:
                print("guess_1 flag")
                flash("Missing Symbol")
                return redirect(url_for('index'))
                #return ('', 204)
                #return redirect("/")
                #return render_template("index.html")
                #return ("Missing symbol")
            else:
                score_res=mainloop.guessloop(secret, guess_1, int(score))
                flash(score_res)
                #score_res-=10
                #print('score_res',score_res)
                #return ('', 204)
                return redirect(url_for('index'))

                '''
                print("int secret out if",int(secret),int(guess_1),int(guess_2))
                if int(secret)!=int(guess_1) and guess_2:
                    print("int secret in if",int(secret),int(guess_1),int(guess_2))
                    score_res=mainloop.guessloop(secret,guess_2,score_res)
                    flash(score_res)
                    return redirect(url_for('index'))
                else:
                    print('flag')
                    flash("Missing Symbol")
                    return redirect(url_for('index'))
                    '''
                #flash(symbol)
                #return redirect("/")
                #return render_template("index.html")






'''
    """Show portfolio of stocks"""
    purchasedict = {}
    holdingdict = {}
    selldict = {}

    # Get stock and shares from 'purchase' table for current user
    stocklist = db.execute(
        "SELECT stock, SUM(share) as shares FROM purchase WHERE  user_id=:user_id GROUP BY stock", user_id=session['user_id'])
    # Keys:symbol, Values:shares
    for item in stocklist:
        purchasedict[item['stock']] = item['shares']

    # Get stock and shares from 'sell' table
    selllist = db.execute("SELECT stock, SUM(share) as shares FROM sell WHERE  user_id=:user_id GROUP BY stock",
                          user_id=session['user_id'])
    for item in selllist:
        selldict[item['stock']] = item['shares']

    # Calculate currently holding shares using ('purchase.shares' + 'sell.shares(negative)')
    for key in purchasedict:
        if key in selldict:
            purchasedict[key] = int(purchasedict[key]) + int(selldict[key])

    # Get stock and shares from 'marketvalue' table
    holdinglist = db.execute("SELECT stock, shares FROM marketvalue WHERE user_id=:user_id", user_id=session['user_id'])
    for item in holdinglist:
        holdingdict[item['stock']] = item['shares']

    # Check stock information
    for k in purchasedict:
        pricedict = lookup(k)
        price = float(pricedict['price'])  # Current stock price
        total = float(int(purchasedict[k]) * price)  # Current stock market value
        name = pricedict['name']  # Symbol company name

    # if purchasedict.keys in holdingdict, update shares in 'marketvalue'
        if k in holdingdict.keys():
            db.execute("UPDATE marketvalue SET shares=:shares, totalvalue=:totalvalue, price=:price WHERE user_id=:user_id AND stock=:stock",
                       shares=purchasedict[k], totalvalue=total, price=price, user_id=session['user_id'], stock=k)
    # if purchasedict.keys not in holdingdict, insert key and value as stock and shares into 'marketvalue'
        else:
            db.execute("INSERT or IGNORE INTO marketvalue (user_id, stock, shares, price, totalvalue, name, currentdate) VALUES (:user_id, :stock, :shares, :price, :totalvalue, :name, CURRENT_TIMESTAMP)",
                       user_id=session['user_id'], stock=k, shares=purchasedict[k], price=price, totalvalue=total, name=name)

    # If stock shares ==0: delete stock record in 'marketvalue'
    db.execute("DELETE FROM marketvalue WHERE user_id=:user_id AND shares=:shares", user_id=session['user_id'], shares=0)

    # Index.html table display
    balance = 0
    holdings = db.execute(
        "SELECT stock, name, shares, price, totalvalue FROM marketvalue WHERE user_id=:user_id GROUP BY stock", user_id=session["user_id"])
    for item in holdings:
        valuefloat = float(item['totalvalue'])
        balance += valuefloat
        item['price'] = usd(item['price'])
        item['totalvalue'] = usd(item['totalvalue'])

    cashdict = db.execute("SELECT cash FROM users WHERE id=:id", id=session['user_id'])
    cash = float(cashdict[0]['cash'])

    # balance is total of all current holding stock value
    balance = round(balance, 2)
    # totalbalance is balance + cash
    totalbalance = round((balance+cash), 2)
    return render_template("index.html", holdings=holdings, cashbalance=usd(cash), totalbalance=usd(totalbalance))
'''

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
        rows = db.execute("SELECT * FROM records WHERE username=:username",
                          username=request.form.get("username"))
                        #"SELECT stock, shares FROM marketvalue WHERE user_id=:user_id",
                        #user_id=session['user_id'])
        testusername=request.form.get("username")
        print(testusername)
        # Ensure username exists and password is correct
        '''if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)'''

        # Remember which user has logged in
        #session["user_id"] = rows[0]["id"]
        print("rows",rows)
        session["id"] = rows[0]["id"]
        # Redirect user to home page
        flash('Logged in!')
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
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        # Ensure username is not blank
        if not username:
            message = "You must provide a username."
            return apology(message)

        # Ensure username is unique
        usernames = db.execute("SELECT username FROM records")
        for row in usernames:
            if username == row['username']:  # row is returned as key-value pairs
                message = "This username has been registered, try another username."
                return apology(message)

        password = request.form.get("password")
        # Ensure password is not blank
        if not password:
            message = "You must provide a password."
            return apology(message)

        confirmation = request.form.get("confirmation")
        # Ensure password confirmation matches with password
        if not confirmation or password != confirmation:
            message = "You must confirm your password."
            return apology(message)

        # Give the password a hash value to be stored in the database
        passhash = generate_password_hash(password)
        db.execute("INSERT INTO records (username, password) VALUES (:username, :password)", username=username, password=passhash)

        # Get session['user_id'] for this registered user, redirect the user to index.html with logged in info.
        # Query database for username
        rows = db.execute("SELECT * FROM records WHERE username = :username",
                          username=username)
        # Remember which user has logged in
        #session["user_id"] = rows[0]["id"]
        session["id"] = rows[0]["id"]
        flash('Registered!')
        return redirect("/")




def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == '__main__':
    app.run(debug=True)
