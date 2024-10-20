from flask import Flask, render_template, request, redirect, session
import MySQLdb

app = Flask(__name__)
app.secret_key = "secret_key" 

db = MySQLdb.connect("localhost", "root", "root", "users_db")

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        mobile_number = request.form['mobile_number']
        password = request.form['password']
        
        cursor.execute("INSERT INTO users (user_id, mobile_number, password) VALUES (%s, %s, %s)", 
                       (user_id, mobile_number, password))
        db.commit()
        return redirect('/')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        
        cursor.execute("SELECT * FROM users WHERE user_id = %s AND password = %s", (user_id, password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user_id
            return redirect('/welcome')
        else:
            return "Login failed. Incorrect UserID or Password."
    
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'user_id' in session:
        return render_template('welcome.html')
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
