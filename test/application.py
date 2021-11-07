import os

import sqlite3
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
#from flask_session import Session
#from tempfile import mkdtemp
#from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import mainloop
import rand
from helpers import login_required, apology

# Configure application
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Ensure templates are auto-reloaded
#app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
'''@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
'''


# Configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# Configure SQLite database
#db = sqlite3.connect("mastermind.db")
#cur=db.cursor()
db = SQL("sqlite:///mastermind.db")

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
        rows = db.execute("SELECT * FROM records WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
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
        db.execute("INSERT INTO records (username, password) VALUES (:username, :password)", username=username, hash=passhash)

        # Get session['user_id'] for this registered user, redirect the user to index.html with logged in info.
        # Query database for username
        rows = db.execute("SELECT * FROM records WHERE username = :username",
                          username=username)
        # Remember which user has logged in
        session["id"] = rows[0]["id"]

        flash('Registered!')
        return redirect("/")




if __name__ == '__main__':
    app.run(debug=True)
