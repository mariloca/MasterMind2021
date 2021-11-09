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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mastermind.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():


    #Get current timestamp and score
    userdict=db.execute("SELECT username FROM user WHERE id=:id", id=session["id"])
    username=userdict[0]['username']
    maxdict=db.execute("SELECT MAX(timestamp) as maxstamp, secret FROM records WHERE username=:username",username=username)
    maxstamp=maxdict[0]['maxstamp']
    # get secret for current timestamp
    secret=maxdict[0]['secret']

    print('maxdict',maxdict)


    mindict=db.execute("SELECT MIN(attempt) as minattempt FROM records WHERE username=:username AND timestamp=:timestamp",
               username=username, timestamp=maxstamp)
    minattempt=mindict[0]['minattempt']

    scoredict=db.execute("SELECT score, attempt FROM records WHERE timestamp=:timestamp AND username=:username AND attempt=:attempt",timestamp=maxstamp, username=username, attempt=minattempt)
    print("scoredict", scoredict)
    score=scoredict[0]["score"]
    attempt=scoredict[0]["attempt"]
    print("score, attempt", score, attempt)
    if score!=0:
        if request.method == "GET":
            #flash(secret)
            #click home button while in index page, nothing happens, refresh current page
            #and rerun sequence above, which resulting the same.
            return render_template("index.html")
        else:
            guess = request.form.get("guess")
            if not guess:
                flash("Missing Symbol")
                #return redirect(url_for('index'))
                #return ('', 204)
                #return redirect("/")
                return render_template("index.html")
            else:
                #Insert each guess into database
                print("current attempt",attempt)
                #Test
                #secret=263
                #Convert int secret to list secret
                secretlist = [str(x) for x in str(secret)]
                # check if MSB == 0
                if secret//1000 == 0:
                    secretlist.insert(0, '0')
                print('secretlist',secretlist)
                score_res=mainloop.guessloop(secretlist, guess, score)

                #score_res.append(guess)
                flash(score_res)
                newscore=score_res[0]
                compareresult=score_res[1][0]
                almost,bingo=score_res[1][1],score_res[1][2]

                attempt = attempt-1
                #score_res-=10
                #print('score_res',score_res)
                #return ('', 204)
                #Add each guess record into database
                db.execute("INSERT OR IGNORE INTO records (username, score, attempt, guess, timestamp, almost, bingo) VALUES (:username, :score, :attempt, :guess, :timestamp, :almost, :bingo)",
                   username=username, score=newscore, attempt=attempt, guess=guess, timestamp=maxstamp, almost=almost, bingo=bingo)

                print("compare result", newscore,compareresult,almost,bingo)
                if compareresult == 1:
                    flash("You win! Let's try again")
                    #need to redirect to restart page and regenerate secret
                    return redirect(url_for('restart'))


                print("after guess attempt", attempt)
                #return ('', 204)

                #Get guess data from database to display in index.html
                holdings = db.execute(
                    "SELECT score, attempt, guess, almost, bingo FROM records WHERE username=:username AND timestamp=:timestamp", username=username, timestamp=maxstamp)
                print("holdings", holdings)
                #return render_template("index.html", holdings=holdings)

                return redirect(url_for('index'))

                #flash(symbol)
                #return redirect("/")
                #return render_template("index.html")
    flash("You failed! Let's try again!")
    #need to redirect to restart page and regenerate secret
    return redirect(url_for('restart'))


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
        '''if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)'''

        # Remember which user has logged in
        #session["user_id"] = rows[0]["id"]
        session["id"] = rows[0]["id"]

        maxtimestamp = db.execute("SELECT MAX(timestamp) as MaxT FROM records WHERE username=:username", username=request.form.get("username"))
        # generate secret in login page and pass into database row
        secretlist=rand.randomnumbergenerate(4,0,7) #Generate random number in a list
        strings = [str(integer) for integer in secretlist]
        a_string = "".join(strings)
        secret = int(a_string)
        print('max',maxtimestamp)
        if maxtimestamp[0]['MaxT']==None:
            db.execute("INSERT or IGNORE INTO records (username, score, attempt, guess, timestamp, almost, bingo, secret) VALUES (:username, :score, :attempt, :guess, :timestamp, :almost, :bingo, :secret)",
               username=request.form.get("username"), score=100, attempt=10, guess=None, timestamp=0, almost=None, bingo=None, secret=secret)

            '''
            test = db.execute("SELECT * FROM records WHERE username=:username", username=request.form.get("username"))
            print("after add new timestamp record", test)
            print("add new timestamp")
            '''
        else:
            currenttimestamp=maxtimestamp[0]['MaxT']+1
            db.execute("INSERT or IGNORE INTO records (username, score, attempt, guess, timestamp, almost, bingo, secret) VALUES (:username, :score, :attempt, :guess, :timestamp, :almost, :bingo, :secret)",
               username=request.form.get("username"), score=100, attempt=10, guess=None, timestamp=currenttimestamp, almost=None, bingo=None, secret=secret)
            print('current',currenttimestamp)
        # Redirect user to home page
        flash('Logged in!')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/restart", methods=["GET", "POST"])
@login_required
def restart():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        '''
        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE username=:username",
                          username=request.form.get("username"))
        # Remember which user has logged in
        session["id"] = rows[0]["id"]
        '''

        userdict=db.execute("SELECT username FROM user WHERE id=:id", id=session["id"])
        username=userdict[0]['username']

        maxtimestamp = db.execute("SELECT MAX(timestamp) as MaxT FROM records WHERE username=:username", username=username)
        # generate secret in restart page and pass into database row
        secretlist=rand.randomnumbergenerate(4,0,7) #Generate random number in a list
        strings = [str(integer) for integer in secretlist]
        a_string = "".join(strings)
        secret = int(a_string)
        print('max',maxtimestamp)
        if maxtimestamp[0]['MaxT']==None:
            db.execute("INSERT or IGNORE INTO records (username, score, attempt, guess, timestamp, almost, bingo, secret) VALUES (:username, :score, :attempt, :guess, :timestamp, :almost, :bingo, :secret)",
               username=username, score=100, attempt=10, guess=None, timestamp=0, almost=None, bingo=None, secret=secret)
        else:
            currenttimestamp=maxtimestamp[0]['MaxT']+1
            db.execute("INSERT or IGNORE INTO records (username, score, attempt, guess, timestamp, almost, bingo, secret) VALUES (:username, :score, :attempt, :guess, :timestamp, :almost, :bingo, :secret)",
               username=username, score=100, attempt=10, guess=None, timestamp=currenttimestamp, almost=None, bingo=None, secret=secret)
            print('current',currenttimestamp)
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
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

        # Get session['user_id'] for this registered user, redirect the user to index.html with logged in info.
        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE username = :username",
                          username=username)
        # Remember which user has logged in
        session["id"] = rows[0]["id"]
        secretlist=rand.randomnumbergenerate(4,0,7) #Generate random number in a list
        strings = [str(integer) for integer in secretlist]
        a_string = "".join(strings)
        secret = int(a_string)
        #Insert timestamp to the new user
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
