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

#message flashing
#https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/

# Configure application
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mastermind.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Get current timestamp as of Max timestamp
    userdict=db.execute("SELECT username FROM user WHERE id=:id", id=session["id"])
    username=userdict[0]['username']
    maxdict=db.execute("SELECT MAX(timestamp) as maxstamp, secret FROM records WHERE username=:username",username=username)
    # Get secret for current timestamp and secret
    maxstamp=maxdict[0]['maxstamp']
    secret=maxdict[0]['secret']
    print("secret", secret) #For demo use
    # Get Min attempt
    mindict=db.execute("SELECT MIN(attempt) as minattempt FROM records WHERE username=:username AND timestamp=:timestamp",
               username=username, timestamp=maxstamp)
    minattempt=mindict[0]['minattempt']

    # Get current score
    scoredict=db.execute("SELECT score, attempt FROM records WHERE timestamp=:timestamp AND username=:username AND attempt=:attempt",timestamp=maxstamp, username=username, attempt=minattempt)
    score=scoredict[0]["score"]
    attempt=scoredict[0]["attempt"]

    if score!=0:
        if request.method == "GET":
            '''
            Click home button while in index page, nothing happens, refresh current page
            and rerun sequence above, which resulting the same.
            '''
            return render_template("index.html")
        else:
            guess = request.form.get("guess")
            # Catch input error
            if not guess:
                flash("Missing guess.")
                return render_template("index.html")
            elif len(str(guess))!=4:
                return apology("Your guess must be a 4 digit number", 403)
            elif guess.isnumeric()==False:
                return apology("You must enter a number", 403)
            else:
                # Insert each guess into database
                '''
                Corner case:
                1. secret=0000
                2. guess=0000
                Solution: change 'secret' and 'guess' type from int to text in database
                '''
                # Convert int secret to list secret
                secretlist = [str(x) for x in str(secret)]

                # Get current guess result
                score_res=mainloop.guessloop(secretlist, guess, score)
                newscore=score_res[0]
                compareresult=score_res[1][0]
                almost,bingo=score_res[1][1],score_res[1][2]
                attempt = attempt-1

                # Add each guess record into database
                db.execute("INSERT OR IGNORE INTO records (username, score, attempt, guess, timestamp, almost, bingo) VALUES (:username, :score, :attempt, :guess, :timestamp, :almost, :bingo)",
                   username=username, score=newscore, attempt=attempt, guess=guess, timestamp=maxstamp, almost=almost, bingo=bingo)


                # Get guess data from database to display in index.html
                holdings = db.execute(
                    "SELECT score, attempt, guess, almost, bingo FROM records WHERE username=:username AND timestamp=:timestamp", username=username, timestamp=maxstamp)
                # Win condition
                if compareresult == 1:
                    flash("You win! Let's try again")
                    # Need to redirect to restart page and regenerate secret
                    return redirect(url_for('restart'))
                # Fail condition
                if newscore==0:
                    flash("You failed! Let's try again!")
                    # Need to redirect to restart page and regenerate secret
                    return redirect(url_for('restart'))

                return render_template("index.html", holdings=holdings)



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
        rows = db.execute("SELECT * FROM user WHERE username=:username",
                          username=request.form.get("username"))


        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["id"] = rows[0]["id"]

        maxtimestamp = db.execute("SELECT MAX(timestamp) as MaxT FROM records WHERE username=:username", username=request.form.get("username"))
        # Generate secret in login page and pass into database row
        secretlist=rand.randomnumbergenerate(4,0,7) #Generate random number in a list

        # Convert str list of secret to int
        strings = [str(integer) for integer in secretlist]
        secret = "".join(strings)

        # Insert new start record when first login
        if maxtimestamp[0]['MaxT']==None:
            db.execute("INSERT or IGNORE INTO records (username, score, attempt, guess, timestamp, almost, bingo, secret) VALUES (:username, :score, :attempt, :guess, :timestamp, :almost, :bingo, :secret)",
               username=request.form.get("username"), score=100, attempt=10, guess=None, timestamp=0, almost=None, bingo=None, secret=secret)
        # Insert new start record and increase timestamp by 1
        else:
            currenttimestamp=maxtimestamp[0]['MaxT']+1
            db.execute("INSERT or IGNORE INTO records (username, score, attempt, guess, timestamp, almost, bingo, secret) VALUES (:username, :score, :attempt, :guess, :timestamp, :almost, :bingo, :secret)",
               username=request.form.get("username"), score=100, attempt=10, guess=None, timestamp=currenttimestamp, almost=None, bingo=None, secret=secret)


        # Redirect user to home page
        flash('Logged in!')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/restart", methods=["GET", "POST"])
@login_required
def restart():

    if request.method == "POST":
        # Get username
        userdict=db.execute("SELECT username FROM user WHERE id=:id", id=session["id"])
        username=userdict[0]['username']

        maxtimestamp = db.execute("SELECT MAX(timestamp) as MaxT FROM records WHERE username=:username", username=username)
        # Generate secret in restart page and pass into database row
        secretlist=rand.randomnumbergenerate(4,0,7) #Generate random number in a list

        # Convert str list of secret to int
        strings = [str(integer) for integer in secretlist]
        secret = "".join(strings)

        # Insert new start record when first login
        if maxtimestamp[0]['MaxT']==None:
            db.execute("INSERT or IGNORE INTO records (username, score, attempt, guess, timestamp, almost, bingo, secret) VALUES (:username, :score, :attempt, :guess, :timestamp, :almost, :bingo, :secret)",
               username=username, score=100, attempt=10, guess=None, timestamp=0, almost=None, bingo=None, secret=secret)
        # Insert new start record and increase timestamp by 1
        else:
            currenttimestamp=maxtimestamp[0]['MaxT']+1
            db.execute("INSERT or IGNORE INTO records (username, score, attempt, guess, timestamp, almost, bingo, secret) VALUES (:username, :score, :attempt, :guess, :timestamp, :almost, :bingo, :secret)",
               username=username, score=100, attempt=10, guess=None, timestamp=currenttimestamp, almost=None, bingo=None, secret=secret)
        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("restart.html")



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
        usernames = db.execute("SELECT username FROM user")
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
        db.execute("INSERT INTO user (username, password) VALUES (:username, :password)", username=username, password=passhash)

        # Get session['id'] for this registered user, redirect the user to index.html with logged in info.
        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE username = :username",
                          username=username)
        # Remember which user has logged in
        session["id"] = rows[0]["id"]
        # Generate random number in a list for every Register and pass to database row
        secretlist=rand.randomnumbergenerate(4,0,7)
        strings = [str(integer) for integer in secretlist]
        secret = "".join(strings)

        #Insert new record to the new user
        db.execute("INSERT or IGNORE INTO records (username, score, attempt, timestamp, secret) VALUES (:username, :score, :attempt, :timestamp, :secret)", username=username, score=100, attempt=10, timestamp=0, secret=secret)

        flash('Registered!')
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
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
