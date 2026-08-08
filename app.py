from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,country_id,email,password,phone) values (:username,:country_id,:email,:password,:phone)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','country_id','email','password','phone']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','country_id','email','password','phone']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','country_id','email','password','phone']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_data", methods=["GET","POST"])
def add_one_data():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into data (user_id,name,value) values (:user_id,:name,:value)",hey)
        user = query_db('select * from data')

        return render_template("dataform.html", datas=user, one_user=one_user, the_title="add new data", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from data')
    one_user = query_db("select * from data limit 1", one=True)
    return render_template("dataform.html", datas=user, one_user=one_user, the_title="add new data", touslesuser=touslesuser)

@app.route("/add_one_device", methods=["GET","POST"])
def add_one_device():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into device (name) values (:name)",hey)
        user = query_db('select * from device')

        return render_template("deviceform.html", devices=user, one_user=one_user, the_title="add new device")


    user = query_db('select * from device')
    one_user = query_db("select * from device limit 1", one=True)
    return render_template("deviceform.html", devices=user, one_user=one_user, the_title="add new device")

@app.route("/add_one_userhasdevice", methods=["GET","POST"])
def add_one_userhasdevice():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesdevice= query_db("select * from device")

        touslesuser= query_db("select * from user")

        one_user = query_db("insert into userhasdevice (device_id,user_id) values (:device_id,:user_id)",hey)
        user = query_db('select * from userhasdevice')

        return render_template("userhasdeviceform.html", userhasdevices=user, one_user=one_user, the_title="add new userhasdevice", touslesdevice=touslesdevice, touslesuser=touslesuser)


    touslesdevice= query_db("select * from device")

    touslesuser= query_db("select * from user")

    user = query_db('select * from userhasdevice')
    one_user = query_db("select * from userhasdevice limit 1", one=True)
    return render_template("userhasdeviceform.html", userhasdevices=user, one_user=one_user, the_title="add new userhasdevice", touslesdevice=touslesdevice, touslesuser=touslesuser)

@app.route("/add_one_airport", methods=["GET","POST"])
def add_one_airport():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescity= query_db("select * from city")

        one_user = query_db("insert into airport (short_name,name,city_id) values (:short_name,:name,:city_id)",hey)
        user = query_db('select * from airport')

        return render_template("airportform.html", airports=user, one_user=one_user, the_title="add new airport", touslescity=touslescity)


    touslescity= query_db("select * from city")

    user = query_db('select * from airport')
    one_user = query_db("select * from airport limit 1", one=True)
    return render_template("airportform.html", airports=user, one_user=one_user, the_title="add new airport", touslescity=touslescity)

@app.route("/add_one_city", methods=["GET","POST"])
def add_one_city():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into city (name,country_id) values (:name,:country_id)",hey)
        user = query_db('select * from city')

        return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from city')
    one_user = query_db("select * from city limit 1", one=True)
    return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city", touslescountry=touslescountry)

@app.route("/add_one_userflights", methods=["GET","POST"])
def add_one_userflights():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesairline_company= query_db("select * from airline_company")

        touslesuser= query_db("select * from user")

        one_user = query_db("insert into userflights (airport1_id,airport2_id,date,heure,number,airline_company_id,user_id) values (:airport1_id,:airport2_id,:date,:heure,:number,:airline_company_id,:user_id)",hey)
        user = query_db('select * from userflights')

        return render_template("userflightsform.html", userflightss=user, one_user=one_user, the_title="add new userflights", touslesairline_company=touslesairline_company, touslesuser=touslesuser)


    touslesairline_company= query_db("select * from airline_company")

    touslesuser= query_db("select * from user")

    user = query_db('select * from userflights')
    one_user = query_db("select * from userflights limit 1", one=True)
    return render_template("userflightsform.html", userflightss=user, one_user=one_user, the_title="add new userflights", touslesairline_company=touslesairline_company, touslesuser=touslesuser)

@app.route("/add_one_airline_company", methods=["GET","POST"])
def add_one_airline_company():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into airline_company (name) values (:name)",hey)
        user = query_db('select * from airline_company')

        return render_template("airline_companyform.html", airline_companys=user, one_user=one_user, the_title="add new airline_company")


    user = query_db('select * from airline_company')
    one_user = query_db("select * from airline_company limit 1", one=True)
    return render_template("airline_companyform.html", airline_companys=user, one_user=one_user, the_title="add new airline_company")

@app.route("/add_one_conversations", methods=["GET","POST"])
def add_one_conversations():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuserhasdevice= query_db("select * from userhasdevice")

        one_user = query_db("insert into conversations (userhasdevice_id,sender,receiver,description) values (:userhasdevice_id,:sender,:receiver,:description)",hey)
        user = query_db('select * from conversations')

        return render_template("conversationsform.html", conversationss=user, one_user=one_user, the_title="add new conversations", touslesuserhasdevice=touslesuserhasdevice)


    touslesuserhasdevice= query_db("select * from userhasdevice")

    user = query_db('select * from conversations')
    one_user = query_db("select * from conversations limit 1", one=True)
    return render_template("conversationsform.html", conversationss=user, one_user=one_user, the_title="add new conversations", touslesuserhasdevice=touslesuserhasdevice)

