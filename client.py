from flask import*
from database import*


client=Blueprint('client',__name__)
@client.route('/client_home')
def client_home():
	return render_template('client_home.html')

@client.route('/cli_manage_cases',methods=['get','post'])
def cli_manage_cases():
	data={}
	client_id=session['client_id']

	if 'submit' in request.form:
		title=request.form['title']
		description=request.form['description']
		case_date=request.form['date']
		police_station=request.form['Police']
		pincode=request.form['Pincode']
		phone=request.form['phone']
		q="INSERT INTO cases(client_id,title,`description`,case_date,police_station,pincode,phone)VALUES('%s','%s','%s','%s','%s','%s','%s')"%(client_id,title,description,case_date,police_station,pincode,phone)
		insert(q)
		return redirect(url_for('client.cli_manage_cases'))

	q="SELECT * FROM cases where client_id='%s'"%(client_id)
	res=select(q)
	data['cases']=res

		
	
	return render_template('cli_manage_cases.html',data=data)
	

@client.route('/cli_view_proposals',methods=['get','post'])
def cli_view_proposals():
	data={}

	ids=request.args['ids']

	if 'action' in request.args:
		action=request.args['action']
		pid=request.args['pid']
		# cid=request.args['cid']
	else:
		action=None

	if action =='accept':
		q="UPDATE `proposals` SET `status`='accepted' WHERE `proposal_id`='%s'"%(pid)
		update(q)
		# q1="UPDATE `cases` SET `status`='accepted' WHERE `case_id`='%s'"%(cid)
		# update(q1)
		
		flash('Accepted...')
		return redirect(url_for('client.client_home'))
	if action=='reject':
		q="UPDATE `proposals` SET `status`='rejected' WHERE `proposal_id`='%s'"%(pid)
		update(q)
		flash('Rejected...')
		return redirect(url_for('client.client_home'))

	q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS adv_name,`proposals`.status AS pstatus FROM `proposals` INNER JOIN `cases` USING (`case_id`)INNER JOIN `adv_registration` USING(`adv_id`) where case_id='%s'"%(ids)
	res=select(q)
	data['proposals']=res
	return render_template('cli_view_proposals.html',data=data)


@client.route('/cli_view_lawdetails')
def cli_view_lawdetails():
	data={}

	q="SELECT * FROM law_details "
	res=select(q)
	data['advocates']=res
	return render_template('cli_view_lawdetails.html',data=data)

@client.route('/cli_view_ongoingcases')
def cli_view_ongoingcases():
	data={}
	login_id=session['login_id']

	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS adv_name FROM `client_assigns` INNER JOIN `cases` USING(`case_id`) INNER JOIN `case_types` USING(`type_id`) INNER JOIN `adv_registration` USING(`adv_id`) WHERE `client_assigns`.`client_id`=(SELECT client_id FROM `cli_registration` WHERE login_id='%s') AND `client_assigns`.`status`='accepted'"%(login_id)
	res=select(q)
	data['on_cases']=res
	return render_template('cli_view_ongoingcases.html',data=data)

@client.route('/cli_view_advocate_details')
def cli_view_advocate_details():
	data={}

	ids=request.args['ids']

	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS adv_name FROM `adv_registration` WHERE `adv_id`='%s'"%(ids)
	res=select(q)
	data['adv_details']=res
	return render_template('cli_view_advocate_details.html',data=data)


@client.route('/cli_view_case_notes')
def cli_view_case_notes():
	data={}

	ids=request.args['ids']

	q="SELECT * FROM `case_notes` WHERE `case_id`='%s'"%(ids)
	res=select(q)
	data['case_notes']=res
	return render_template('cli_view_case_notes.html',data=data)

@client.route('/cli_view_case_files')
def cli_view_case_files():
	data={}
	

	ids=request.args['ids']

	
	q="SELECT * FROM `case_files` WHERE `case_id`='%s'"%(ids)
	res=select(q)
	data['case_files']=res
	return render_template('cli_view_case_files.html',data=data)


@client.route('/cli_rate_adv',methods=['get','post'])
def cli_rate_adv():
	data={}
	client_id=session['client_id']
	ids=request.args['ids']

	if 'submit' in request.form:
		rate=request.form['rate']
		review=request.form['review']

		q="INSERT INTO `ratings`(`client_id`,`adv_id`,`rate`,`review`,`date_time`) VALUES('%s','%s','%s','%s',NOW())"%(client_id,ids,rate,review)
		insert(q)
		return redirect(url_for('client.cli_rate_adv',ids=ids))

	q="SELECT *,CONCAT(`adv_registration`.`first_name`,' ',`adv_registration`.`last_name`) AS adv_name,CONCAT(`cli_registration`.`first_name`,' ',`cli_registration`.`last_name`) AS cli_name FROM `ratings` INNER JOIN `cli_registration` USING(`client_id`) INNER JOIN `adv_registration` USING(`adv_id`) WHERE `adv_id`='%s'"%(ids)
	res=select(q)
	data['rating']=res

	return render_template('cli_rate_adv.html',data=data)

@client.route('/cli_view_adv_assigncases')
def cli_view_adv_assigncases():
	data={}

	q="SELECT * FROM client_assigns "
	res=select(q)
	data['advocates']=res
	return render_template('cli_view_adv_assigncases.html',data=data)

@client.route('/cli_snd_comp_viewreply',methods=['get','post'])
def cli_snd_comp_viewreply():
	data={}

	q="SELECT * FROM complaints "
	res=select(q)
	data['complaints']=res
	
	if 'submit' in request.form:
		desc=request.form['description']
		q="INSERT INTO complaints(client_id,`desc`,reply,date_time)VALUES('%s','%s','pending',NOW())"%(session['client_id'],desc)
		insert(q)
		return redirect(url_for('client.cli_snd_comp_viewreply'))

	return render_template('cli_snd_comp_viewreply.html',data=data)

@client.route('/cli_chat',methods=['get','post'])
def cli_chat():
	data={}

	#cid=request.args['cid']
	#qry="select *,concat(first_name,' ',last_name) as name from patients where patient_id='%s'"%(cid)
	#result=select(qry)
	#data['name']=result

	if 'submit' in request.form:
		message=request.form['msg']
		q2="INSERT INTO chat(sender_id,sender_type,receiver_id,receiver_type,message,`date_time`)VALUES('%s','doctor','%s','patient','%s',NOW())"%(session['did'],cid,message)
		insert(q2)
		return redirect(url_for('doctor.doctor_chat_message',cid=cid))

	q="SELECT * FROM chats WHERE (`sender_id`='%s' AND sender_type='doctor' AND `receiver_id`='%s') OR (`sender_id`='%s' AND `receiver_id`='%s' AND receiver_type='doctor')"%(session['did'],cid,cid,session['did'])
	res=select(q)
	data['msg']=res

	return render_template("doctor_chat_message.html",data=data)


@client.route('/client_chat_advocate',methods=['get','post'])
def client_chat_advocate():
	data={}

	client_id=session['client_id']
	advocate_id=request.args['advocate_id']
	qry="SELECT CONCAT(first_name,' ',last_name) AS NAME FROM adv_registration WHERE adv_id='%s'"%(advocate_id)
	result=select(qry)
	data['name']=result

	if 'submit' in request.form:
		message=request.form['msg']

		# todo
		# add receiver id in args

		q2="INSERT INTO chats(sender_id,sender_type,receiver_id,receiver_type,message,`date_time`)VALUES('%s','client','%s','advocate','%s',NOW())"%(session['client_id'],advocate_id,message)
		insert(q2)
		return redirect(url_for('client.client_chat_advocate',advocate_id=advocate_id))

	# todo
	# add receiver id in args

	q="SELECT * FROM chats WHERE (`sender_id`='%s' AND sender_type='client' AND `receiver_id`='%s') OR (`sender_id`='%s' AND `receiver_id`='%s' AND receiver_type='client')"%(client_id,advocate_id,advocate_id,client_id)
	res=select(q)
	data['msg']=res

	return render_template("cli_chat_adv.html",data=data)

@client.route('/client_view_advocates',methods=['get','post'])
def client_view_advocates():

	data={}

	q="SELECT * FROM adv_registration"
	res=select(q)
	data['advocates']=res


	return render_template("client_view_advocates.html",data=data)


@client.route('/client_assign_case_adv',methods=['get','post'])
def client_assign_case_adv():
	data={}
	client_id=session['client_id']
	# aid=request.args['aid']

	if 'action' in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None

	if action=='assign':
		q1="INSERT INTO `client_assigns`(`client_id`,`adv_id`,`case_id`,`date_time`,`status`) VALUES('%s','1','%s',NOW(),'pending')"%(client_id,cid)
		insert(q1)
		return redirect(url_for('client.client_view_advocates'))

	q="SELECT * FROM `cases` INNER JOIN `case_types` USING (`type_id`) WHERE `client_id`='%s' AND `status`='pending'"%(client_id)
	res=select(q)
	data['case']=res




	return render_template("client_assign_case_adv.html",data=data)





