from flask import *
from database import*
public=Blueprint('public',__name__)

@public.route('/')
def dashboard():
	return render_template('dashboard.html')
@public.route('/home')
def home():
	return render_template('homepage.html')
@public.route('/login',methods=['get','post'])
def login():
	
	if 'submit' in request.form:
		uname=request.form['username']
		passwd=request.form['password']

		q="SELECT * FROM login WHERE username='%s' AND password='%s'"%(uname,passwd)
		res=select(q)
		if res:
			session['login_id']=res[0]['login_id']
			if res[0]['user_type']=='admin':
				flash("Logged in Sucessfully!")
				return redirect(url_for('admin.admin_home'))
			
			elif res[0]['user_type']=='advocate':
				q1="SELECT adv_id FROM adv_registration WHERE login_id='%s'"%(session['login_id'])
				res=select(q1)
				session['adv_id']=res[0]['adv_id']	
				flash("Logged in Sucessfully!")
				return redirect(url_for('advocates.advocates_home'))
			
			elif res[0]['user_type']=='client':
				q="SELECT client_id FROM cli_registration WHERE login_id='%s'"%(session['login_id'])
				res=select(q)
				session['client_id']=res[0]['client_id']
				flash("Logged in Sucessfully!")
				return redirect(url_for('client.client_home'))

	return render_template('login.html')

@public.route('/register',methods=['get','post'])
def register():
	if 'submit' in request.form:
		fname=request.form['firstname']
		lname=request.form['lastname']
		quali=request.form['qualification']
		sex=request.form['gender']
		ph=request.form['phone']
		mail=request.form['email']
		hname=request.form['housename']
		place=request.form['place']
		passwd=request.form['password']

		q="INSERT INTO login(username,PASSWORD,user_type)VALUES('%s','%s','pending')"%(mail,passwd)
		id=insert(q)
		q="INSERT INTO adv_registration(login_id,first_name,last_name,qualification,gender,phone,email,house_name,place,status)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','pending')"%(id,fname,lname,quali,sex,ph,mail,hname,place)
		insert(q)
		flash("Submitted Sucessfully!")
		return redirect(url_for('public.register'))

	
	return render_template('register.html')

@public.route('/cli_register',methods=['get','post'])
def cli_register():
	if 'submit' in request.form:
		fname=request.form['firstname']
		lname=request.form['lastname']
		sex=request.form['gender']
		dob=request.form['dob']
		ph=request.form['phone']
		mail=request.form['email']
		hname=request.form['housename']
		place=request.form['place']
		pin=request.form['pincode']
		passwd=request.form['password']

		q="INSERT INTO login(username,PASSWORD,user_type)VALUES('%s','%s','client')"%(mail,passwd)
		id=insert(q)
		q1="INSERT INTO cli_registration(login_id,first_name,last_name,gender,dob,phone,email,house_name,place,pincode)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(id,fname,lname,sex,dob,ph,mail,hname,place,pin)
		insert(q1)
		flash("Submitted Sucessfully!")
		return redirect(url_for('public.cli_register'))
	
	return render_template('cli_register.html')

