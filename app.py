import os 
 
import pymysql
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__) 
app.secret_key = os.environ.get("SECRET_KEY", "") 
 
 
def get_db(): 
    return pymysql.connect( 
        host=os.environ.get("DB_HOST", ""), 
        port=int(os.environ.get("DB_PORT", "")), 
        user=os.environ.get("DB_USER", ""), 
        password=os.environ.get("DB_PASSWORD", ""), 
        database=os.environ.get("DB_NAME", ""), 
        cursorclass=pymysql.cursors.DictCursor, 
    ) 
 

@app.route("/") 
def index(): 
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


 
@app.route("/signup", methods=["GET", "POST"]) 
def signup(): 
    if request.method == "POST": 
        username = request.form["username"].strip() 
        email = request.form["email"].strip().lower() 
        first_name = request.form["first_name"].strip() 
        last_name = request.form["last_name"].strip() 
        password = request.form["password"] 
        confirm_password = request.form["confirm_password"]
 
        if not username or not email or not first_name or not last_name or len(password) < 8:
            return render_template("signup.html") 
        if password != confirm_password:
            return render_template("signup.html")
 
        conn = get_db() 
        try: 
            with conn.cursor() as cur: 
                cur.execute( 
                    "INSERT INTO users (username, first_name, last_name, email, password_hash) " 
                    "VALUES (%s, %s, %s, %s, %s)", 
                    (username, first_name, last_name, email, generate_password_hash(password)), 
                ) 
            conn.commit() 
        except pymysql.err.IntegrityError: 
            return render_template("signup.html") 
        finally: 
            conn.close() 
 
        return redirect(url_for("login")) 
 
    return render_template("signup.html") 
 
 
@app.route("/login", methods=["GET", "POST"]) 
def login(): 
    if request.method == "POST": 
        username = request.form["username"].strip() 
        password = request.form["password"] 
 
        conn = get_db() 
        with conn.cursor() as cur: 
            cur.execute( 
                "SELECT id, username, password_hash FROM users WHERE username = %s", 
                (username,), 
            ) 
            user = cur.fetchone() 
        conn.close() 
 
        if user and check_password_hash(user["password_hash"], password): 
            session.clear() 
            session["user_id"] = user["id"] 
            session["username"] = user["username"] 
            return redirect(url_for("index"))
 
 
    return render_template("login.html") 
 
@app.route("/pokemon/<int:pokemon_id>")
def pokemon(pokemon_id):
    return render_template("pokemon.html", pokemon_id=pokemon_id)

@app.route('/pokeball.jpeg')
def favicon():
    try:
        return send_from_directory(
            directory=app.static_folder,  
            filename='pokeball.jpeg',       
            mimetype='image/vnd.microsoft.icon'
        )
    except FileNotFoundError:
        return '', 404  

if __name__ == "__main__":
    app.run(debug=True)

