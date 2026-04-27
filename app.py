from flask import Flask, render_template,request,redirect
import pandas as pd

import mysql.connector
url ="Apple_data.csv"
df = pd.read_csv(url)
print(df)

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root@Admin1",
    database = "storage"
)
cursor = db.cursor()


app = Flask(__name__)

@app.route("/")
def index(): 
    return render_template("index.html")



@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        query = "INSERT INTO user(name,email,password) VALUES (%s,%s,%s)"
        values = (name,email,password)
        cursor.execute(query, values)
        db.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        query = "SELECT * FROM user WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        if user:
                return redirect("/dashboard")
        else:

            return "Invalid details"
            
    return render_template("login.html")

@app.route("/dashboard")
def home():
    table = df.to_html(classes='data', index=False)
    return render_template("dashboard.html", table=table)
   

if __name__== "__main__":
    app.run(debug=True)
