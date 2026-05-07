from flask import Flask, render_template, request, redirect
import mysql.connector
import pickle

app = Flask(__name__)

# DATABASE 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manshi@ma2",
    database="patient_health_system"
)

cursor = db.cursor()

#ML MODEL 
model = pickle.load(open("models/disease_model.pkl", "rb"))

# HOME 
@app.route("/")
def home():
    return redirect("/login")   # always start from login


# REGISTER 
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        email = request.form["email"]
        password = request.form["password"]

        # insert into database
        query = "INSERT INTO patients (name, age, gender, email, password) VALUES (%s,%s,%s,%s,%s)"
        values = (name, age, gender, email, password)

        cursor.execute(query, values)
        db.commit()

        return redirect("/login")   # after register go to login

    return render_template("register.html")


#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        query = "SELECT * FROM patients WHERE email=%s AND password=%s"
        values = (email, password)

        cursor.execute(query, values)
        user = cursor.fetchone()

        if user:
            return redirect("/dashboard")   # success
        else:
            return render_template("login.html", error="Invalid Email or Password")

    return render_template("login.html")


#DASHBOARD
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# PREDICT
@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":

        symptoms = request.form.getlist("symptoms")

        features = ["fever", "cough", "headache", "fatigue", "vomiting"]

        input_data = []
        for f in features:
            if f in symptoms:
                input_data.append(1)
            else:
                input_data.append(0)

        prediction = model.predict([input_data])[0]

        symptoms_str = ", ".join(symptoms)

        # TEMP patient id
        patient_id = 1

        query = "INSERT INTO prediction_history (patient_id, symptoms, predicted_disease) VALUES (%s, %s, %s)"
        values = (patient_id, symptoms_str, prediction)

        cursor.execute(query, values)
        db.commit()

        return render_template("result.html", disease=prediction)

    return render_template("predict.html")


#  HISTORY 
@app.route("/history")
def history():

    query = "SELECT * FROM prediction_history"
    cursor.execute(query)
    data = cursor.fetchall()

    return render_template("history.html", records=data)


#RUN
if __name__ == "__main__":
    app.run(debug=True)