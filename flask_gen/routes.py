from os import spawnl
from flask import render_template, url_for, request, redirect, flash, jsonify
from flask_gen import app, db, bcrypt, csrf
from flask_gen.models import User
from flask_login import login_required, login_user, logout_user, current_user
import sqlite3
from flask_cors import cross_origin
import datetime


def connect():
    conn = sqlite3.connect('./farmer-mgmt/database.db')
    c = conn.cursor()
    return c, conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Invalid Credentials!")
        elif user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index')) if user.usertype != "admin" else redirect(url_for('adminpage'))
        elif bcrypt.check_password_hash(user.password, password) == False:
            flash('Entered password is wrong. Please try again.')
        return redirect(url_for("adminpage"))
    else:
        return render_template('adminauth.html')


@app.route('/adminpage')
@login_required
def adminpage():
    data = User.query.all()
    return render_template('admin.html', users=data)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        dob = request.form['dob']
        name = request.form['name']
        income = request.form['income']
        aadhar = request.form['aadhar']
        phno = request.form['phno']
        user = User(aadhar=aadhar, username=username, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        if user.query.filter_by(username = username).first():
            flash("Username Already Exists.")
            return redirect(url_for("authenticate"))
        elif user.query.filter_by(aadhar = aadhar).first():
            flash("Aadhar number already registered!")
            return redirect(url_for("authenticate"))

        else:
            c,conn=connect()
            c.execute(f'insert into users values("{username}","{password}","{name}","{income}","{dob}","{aadhar}","{phno}")')

            db.session.add(user)
            db.session.commit()
            conn.commit()
            flash("Your account has been created.. You can now login.")
            conn.close()
            return redirect("authenticate")


@app.route('/login', methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user_home"))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("user_home"))
        else:
            flash("Wrong Credentials!")
            return redirect(url_for("authenticate"))


    return render_template('login.html')

@app.route('/authenticate')
def authenticate():
    if current_user.is_authenticated:
        return redirect(url_for("user_home"))
    return render_template('login.html')


@app.route('/user-home')
@login_required
def user_home():
    c,conn=connect()
    # We havent set up logout yet
    # line 40
    c.execute(f"select * from users where username like '{current_user.username}'")
    userdet=c.fetchall()
    conn.close()
    print(userdet)
    return render_template('user-home.html',data=userdet[0])

@app.route('/shopping')
@login_required
def shopping():
    c, conn =connect()
    c.execute("Select * from seed_fert_det")
    details=c.fetchall()
    seeds,fert=[],[]
    for det in details:
        if det[3].lower()=='seed':
            seeds.append(det)
        else:
            fert.append(det)
    c.execute('Select * from purchases')
    purchases = c.fetchall()
    user_history=[]
    for i in purchases:
        if i[1]==current_user.username:
            user_history.append(i)
    conn.close()

    return render_template('shopping.html',seeds=seeds,fert=fert,history=user_history)


@app.route('/rent', methods=["POST"])
@csrf.exempt
def rent():
    machineid = eval(str(request.data.decode("utf-8")))
    print(machineid)
    machineid["id"] = machineid["id"].strip()
    current_time = datetime.datetime.now()
    print(machineid)
    c,conn=connect()
    c.execute('select * from rents')
    rents=c.fetchall()
    rentid=int(rents[-1][0])
    rentid+=1
    for i in rents:
        print(i)
        print()
    c.execute("select * from machinery")
    machinery=c.fetchall()
    for i in machinery:
        if i[0]==machineid['id']:
            cost=i[1]
    c.execute(f'insert into rents values("{rentid}","{current_user.username}","{machineid["id"]}","{cost}","{current_time.year}-{current_time.month}-{current_time.day}","{machineid["date"]}")')
    conn.commit()
    conn.close()
    return jsonify({"data":"hello"})

@app.route('/buy', methods=["POST"])
@csrf.exempt
def buy():
    itemid = request.data.decode("utf-8")
    current_time = datetime.datetime.now()
    c,conn=connect()
    c.execute('select * from purchases')
    bills=c.fetchall()
    billid=int(bills[-1][0])
    billid+=1
    for i in bills:
        print(i)
    c.execute("select * from seed_fert_det")
    sfdet=c.fetchall()
    for i in sfdet:
        if i[0]==itemid:
            cost=i[1]

    c.execute(f'insert into purchases values("{billid}","{current_user.username}","{itemid}","{current_time.year}-{current_time.month}-{current_time.day}","{cost}")')
    conn.commit()
    conn.close()
    return jsonify({"data":"hello"})



@app.route('/enroll', methods=["POST"])
@csrf.exempt
def enroll():
    data=request.data.decode("utf-8").strip()
    c,con = connect()
    c.execute('select * from govtschemes')
    schemes=c.fetchall()
    for i in schemes:
        print(i)
    c.execute('select * from enrolls')
    enrollments=c.fetchall()
    for i in enrollments:
        print(i)
    enrollid=int(enrollments[-1][0])
    # print(enrollid)
    enrollid+=1
    c.execute(f"insert into enrolls values('{enrollid}','{data}','{current_user.username}')")
    print('hi')
    con.commit()
    con.close()
    return jsonify({"data":"hello"})

@app.route('/renting')
@login_required
def renting():
    cur, database=connect()
    cur.execute('select * from machinery')
    data1 = cur.fetchall()
    cur.execute('select * from rents')
    data2 = cur.fetchall()
    database.close()
    data3=[]
    print(data1,'\n',data2)
    for j in data1:
        if j[0] in [i[2] for i in data2]:
            data3.append('Unavailable')
        else:
            data3.append('Available')
    print(data3)
    history=[]
    for i in data2:
        if i[1]==current_user.username:
            history.append(list(i))
    return render_template('rent.html', data=data1, av=data3,history=history)

@app.route('/govtschemes')
@login_required
def govtschemes():
    c,con = connect()
    c.execute('select * from govtschemes')
    scheme=c.fetchall()
    for i in range(len(scheme)):
        scheme[i]=list(scheme[i])
        print(i)
    schemes = list(scheme)
    c.execute("select * from enrolls")
    enrollments=c.fetchall()
    for i in enrollments:
        print(i)
    con.close()
    for i in schemes:
        print("HERE",[x[1] for x in enrollments if x[2]==current_user.username])
        if i[0] in [x[1] for x in enrollments if x[2]==current_user.username]:
            i.append('unavailable')
        else:
            i.append('available')
    for i in schemes:
        print(i)
    return render_template('govtscheme.html',data=schemes)
