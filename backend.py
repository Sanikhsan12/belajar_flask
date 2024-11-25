# library
from flask import Flask, render_template, request, session, redirect, url_for
from admin import data_admin
import os

app = Flask(__name__, template_folder='frontend/html', static_folder='frontend/css')
app.secret_key = os.urandom(24)

# ? autentikasi
def autentication(username, password):
    for key, value in data_admin.items():
        if username == value['username'] and password == value['password']:
            session['username'] = username
            session['password'] = password
            session['nama'] = key
            return True
    return False

# ! route
@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # fetching data from admin.py
        if autentication(username, password):
            print('login berhasil')
            return redirect(url_for('main'))
        else:
            print('login gagal')
            return render_template('login.html')
    else:   
        return render_template('login.html')

@app.route('/main', methods=['POST','GET'])
def main():
    if 'username' in session and 'password' in session:
        print('session ada')
        nama = session.get('nama')
        return render_template('main.html', nama=nama)
    return redirect(url_for('login'))

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        username = request.form['username']
        password = request.form['password']
        data_admin[nama] = {
            'username' : username,
            'password' : password
        }
        print(f'data baru berhasil di post ke dictionary')
        return render_template('login.html')
    else:
        return render_template('register.html')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('nama', None)
    return redirect(url_for('login'))

# ! run the app
if __name__ == '__main__':
    app.run(debug=True)