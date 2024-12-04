from flask import Flask, render_template, request, jsonify, session, url_for
import razorpay
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123#@Developer'
app.config['MYSQL_DB']='project1'
mysql=MySQL(app)
app.secret_key = "123#@Developer"

@app.route("/")
def index():
    email=session.get('email')
    if email:
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE email=%s',(email,));
        db_data=cur.fetchall()
        return render_template('index_after_login.html', data=db_data[0][1]);
    else:
        return render_template('index.html')

@app.route("/registration",methods=['POST'])
def registration():
    data=request.get_json()
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM user WHERE email=%s or phone=%s',(data['email'],data['phone'],));
    db_data=cur.fetchall()
    if len(db_data)>0:
        return jsonify(False);
    cur.execute('INSERT INTO user(full_name,phone,password,email,address)VALUES(%s,%s,%s,%s,%s)',(data['full_name'].lower(),data['phone'],data['password'],data['email'].lower(),data['address'].lower()))
    mysql.connection.commit()
    cur.close()
    return jsonify(True);

@app.route("/login")
def login():
    email=session.get('email')
    if email:
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE email=%s',(email,));
        db_data=cur.fetchall()
        return render_template('index_after_login.html', name=db_data[0][1]);
    else:
        return render_template('login.html')

@app.route("/login_validation",methods=['POST'])
def login_validate():
    data=request.get_json()
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM user WHERE email=%s and password=%s',(data['email'],data['password'],));
    db_data=cur.fetchall()
    cur.close()
    if len(db_data)>0:
        session['email']=data['email']
        return jsonify({'success': True,'redirect_url': '/index_after_login'})
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password'})

@app.route("/index_after_login")
def index_after_login():
    email=session.get('email')
    if email:
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE email=%s',(email,));
        db_data=cur.fetchall()
        return render_template('index_after_login.html', data=db_data[0]) 
    else:
        return render_template('index.html') 
    
@app.route("/payment", methods=['POST'])
def payment():
    KEY_ID = "rzp_test_HXime5Fpc5G6bn"
    KEY_SECRET = "bCpd6Z149g3nWZ3EcdkqNx0N"
    data=request.get_json()
    razorpay_client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
    amount = int(data['price']) * 100
    courseName=data['courseName']  
    currency = "INR"
    receipt = "order_rcptid_11"
    notes = {"purpose": "Payment for product"}
    order = razorpay_client.order.create({
        "amount": amount,
        "currency": currency,
        "receipt": receipt,
        "notes": notes
    })
    data={
        'order_details':order,
        'key_details':KEY_ID
    }
    return jsonify(data)


@app.route("/logout")
def logout():
    session.clear();
    return render_template("index.html");
if __name__=="__main__":
    app.run(debug=True)