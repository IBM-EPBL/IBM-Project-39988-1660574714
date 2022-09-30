from flask import Flask, render_template, request
import ibm_db

app = Flask(__name__)

conn = ibm_db.connect(
    "DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;"
    "PORT=31198;SECURITY=SSL;SSLServerCertificate"
    "=DigiCertGlobalRootCA.crt;UID=yvm70187;PWD=59EVXEnKnTAAw2oN",
    '', '')
autocommitstatus = ibm_db.autocommit(conn)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        select_sql = 'SELECT firstname FROM USER_DETAIL WHERE email=? AND password=?'
        stmt = ibm_db.prepare(conn, select_sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        d = ibm_db.fetch_assoc(stmt)

        if d:
            return render_template('sample.html', message="Welcome" + " " + d['FIRSTNAME'])
        else:
            return render_template('sample.html', message="Invalid Username or Password")


@app.route('/register')
def register_form():
    return render_template('registrations/user_registration.html')


@app.route('/formreg', methods=['POST', 'GET'])
def addform():
    if request.method == "POST":
        firstname = request.form['fname']
        lastname = request.form['lname']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        password = request.form['password1']
        password2 = request.form['password2']

        sql = 'SELECT * FROM USER_DETAIL WHERE email=?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        flag = ibm_db.fetch_assoc(stmt)

        if flag:
            return render_template('sample.html', message='User already exist')
        else:
            insert_sql = "INSERT INTO USER_DETAIL VALUES (?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, firstname)
            ibm_db.bind_param(prep_stmt, 2, lastname)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, phonenumber)
            ibm_db.bind_param(prep_stmt, 5, password)
            ibm_db.execute(prep_stmt)

            return render_template('sample.html', message='New User Created')
