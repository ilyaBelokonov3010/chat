from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import pickle, json, db_lib

app = Flask(__name__)

db = db_lib.db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        print('[LOG] get request, sending a template..')
        return render_template('login.html', additionally='')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        print('breakpoint')
        breakpoint() 
        result = db.login_session(username, password)
        if result == None:
            response = render_template('login.html', additionally = '<p style="color: red;">Wrong username or password</p>')
        else:
            response = make_response(render_template())
    
    response.set_cookie('session', username, max_age=31536000, httponly=True)
    
    return response

@app.route('/', methods=['GET', 'POST'])
def request_processing():
   if request.method == 'POST':
        msg = request.form.get('message')
        if msg:
            pass
        return redirect('/')

   if request.method == 'GET':
        session_id = request.cookies.get('session')
        return redirect('/login')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)