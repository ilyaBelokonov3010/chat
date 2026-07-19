from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import pickle, json, db_lib, atexit, sys, signal, time

app = Flask(__name__)
db = db_lib.db()

def safe_exit_handler(signum=None, frame=None):
    print("\n[СИСТЕМА] Сохранение базы данных перед выходом...")
    db.save()
    if signum:  # Если завершение вызвано сигналом ОС (Ctrl+C)
        sys.exit(0)

atexit.register(safe_exit_handler)
signal.signal(signal.SIGINT, safe_exit_handler)
signal.signal(signal.SIGTERM, safe_exit_handler)

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
        result = db.get_session(username, password)
        if result == None:
            response = render_template('login.html', additionally = '<p style="color: red;">Wrong username or password</p>')
        else:
            response = make_response(render_template('main.html', additionally = db.render_messages))
    
    response.set_cookie('session', username, max_age=31536000, httponly=True)
    
    return response

@app.route('/', methods=['GET', 'POST'])
def request_processing():
   if request.method == 'POST':
        msg = request.form.get('message')
        if msg:
            token = request.cookies.get('session')
            if token:
                session = db.login_session(token)
                if session:
                    new_message = {
                        "text": msg,
                        "user_id": session.user.id,
                        "time": time.time()
                                    }
                    db.messages[len(db.messages)] = new_message
                return  render_template('main.html', additionally = db.render_messages, account =  session.user)
            else:
                return redirect('/login')
        return redirect('/')

   if request.method == 'GET':
        session_id = request.cookies.get('session')
        if session_id:
            return render_template('main.html', additionally = db.render_messages, account =  db.get_session(session_id).user)
        return redirect('/login')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)