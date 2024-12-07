from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_mail import Mail, Message
import razorpay
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import secrets

load_dotenv()
app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123#@Developer'
app.config['MYSQL_DB']='project1'
mysql=MySQL(app)
app.secret_key = secrets.token_hex(16)
KEY_ID = "rzp_test_HXime5Fpc5G6bn"
KEY_SECRET = "bCpd6Z149g3nWZ3EcdkqNx0N"
razorpay_client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

@app.route("/")
def index():
    email=session.get('email')
    if email:
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE email=%s',(email,));
        db_data=cur.fetchall()

        cur.execute('SELECT * FROM courses');
        courses=cur.fetchall()

        cur.execute('SELECT * FROM user_courses WHERE user_id=%s',(db_data[0][0],));
        user_courses=cur.fetchall()

        purchased_courses={}
        for course in user_courses:
            purchased_courses[course[1]]=True

        remaining_courses=[]
        for course in courses:
            if not course[0] in purchased_courses:
                remaining_courses.append(course)
        return render_template('index_after_login.html', data=db_data[0], courses=remaining_courses);
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
        return redirect(url_for('index'))
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
        return jsonify({'success': True,'redirect_url': '/'})
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password'})
    
@app.route("/payment", methods=['POST'])
def payment():
    data=request.get_json()
    amount = int(data['price']) * 100
    courseDetails=data['courseName']  
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

@app.route("/success",methods=['POST'])
def success():
    data=request.get_json()
    dataDict={
        'razorpay_payment_id':data['paymentId'],
        'razorpay_order_id': data['orderId'],
        'razorpay_signature': data['signature']
    }
    if razorpay_client.utility.verify_payment_signature(dataDict):
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO user_courses(user_id, course_id) VALUES (%s,%s)',(data['user_id'], data['course_id'],));
        mysql.connection.commit()

        cur.execute('SELECT full_name, email FROM user WHERE user_id=%s',(data['user_id'],));
        data=cur.fetchall()[0][0]
        userName=data[0][0]
        email=data[0][1]

        cur.execute('SELECT course_name FROM courses WHERE id=%s',(data['course_id'],));
        courseName=cur.fetchall()[0][0]

        cur.close()
        sendMail(userName, courseName, email)
        return jsonify(True)
    else:
        print(False)

def sendMail(userName, courseName, email):
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'pamirghosh.official@gmail.com'
    app.config['MAIL_PASSWORD'] = 'lpps xoxq reja lfmn'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app) 
    msg = Message( 
                subject='Course Purchase Confirmation',
                sender ='pamirghosh.official@gmail.com', 
                recipients = [email] 
               ) 
    msg.html = f'''
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <div style="background-color: #f4f4f4; padding: 20px;">
                        <h2 style="color: #333;">Hi {userName.upper()},</h2>
                        <p style="color: #555;">Thank you for purchasing the <strong>{courseName}</strong> course!</p>
                        <p style="color: #555;">You will receive notifications for live classes soon.</p>
                        <br>
                        <footer style="color: #888;">
                            <p>Regards,<br>DebTraders</p>
                        </footer>
                    </div>
                </body>
                </html>
                '''
    mail.send(msg) 

@app.route("/logout")
def logout():
    session.clear();
    return render_template("index.html");
if __name__=="__main__":
    app.run(debug=True)
