import os
import mysql.connector
from flask import Flask, render_template, session, request, redirect
from flask_material import Material


cursor = sql_db.cursor()

app = Flask(__name__)
app.secret_key = os.urandom(24)
Material(app)


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        query =  'SELECT * FROM user where username =\'' + str(username) + '\' AND password = \'' + str(password) + '\''
        print (query)
        cursor.execute(query)
        result_sql = cursor.fetchall()
        print (result_sql[0])
        if not result_sql:
            invalid_credentials = "Invalid Credentials"
            return render_template('login.html', invalid_credentials=invalid_credentials)

        # print (result_sql)
        session['user'] = result_sql[0][0]
        return redirect('/index')
    return render_template('login.html')


@app.route('/index')
def index():
    return render_template('index.html')


# @app.route('/working')
# def working():
#   return render_template('working.html')

@app.route('/counselling', methods=['POST', 'GET'])
def counselling():
    if request.method == 'POST':
        fullname = request.form.get('fullname', '')
        address = request.form.get('add1', '') + ' ' + request.form.get('add2', '')
        info = request.form.get('info', '')
        services = request.form.getlist('services')
        service_str = '|'.join(services)
        print (service_str)
        if not info:
            return render_template('counselling.html', error="Mandatory fields missing")
        query = 'INSERT into counselling(fullname, address, info, services) values (%s, %s, %s, %s)'
        value = (fullname, address, info, service_str)     
        cursor.execute(query, value)
        sql_db.commit()
        return render_template('counselling.html', success="Recorded added successfully")
    return render_template('counselling.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    field_error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            query = 'SELECT * from user where username = \'' + str(username) + '\''
            cursor.execute(query)
            result_sql = cursor.fetchall()

            if result_sql:
                user_exists = "User already exists"
                return render_template('register.html', user_exists=user_exists)
            query = 'INSERT into user(username, password) values (%s, %s)'
            value = (username, password)
            cursor.execute(query, value)
            sql_db.commit()
            return redirect('/login')
        else:
            field_error = "Please check all the fields"
    return render_template('register.html', field_error=field_error)

if __name__ == '__main__':
    app.run(debug=True)
