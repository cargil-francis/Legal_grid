from flask import*
from database import*
import uuid

advocates=Blueprint('advocates',__name__)

@advocates.route('/advocates_home')
def advocates_home():
	return render_template('advocates_home.html')

@advocates.route('/adv_view_casetypes')
def adv_view_casetypes():
	data={}

	q="SELECT * FROM case_types"
	res=select(q)
	data['advocates']=res
	return render_template('adv_view_casetypes.html',data=data)

@advocates.route('/adv_view_lawdetails')
def adv_view_lawdetails():
	data={}

	q="SELECT * FROM law_details "
	res=select(q)
	data['advocates']=res
	return render_template('adv_view_lawdetails.html',data=data)

@advocates.route('/adv_view_usercases')
def adv_view_usercases():
	data={}

	q="SELECT * FROM `cases` "
	res=select(q)
	data['cases']=res
	return render_template('adv_view_usercases.html',data=data)

@advocates.route('/adv_view_client_assigncases')
def adv_view_client_assigncases():
	data={}
	a_id=session['adv_id']

	if 'action' in request.args:
		action=request.args['action']
		ids=request.args['ids']
		cid=request.args['cid']
	else:
		action=None

	if action == 'accept':
		q="UPDATE `client_assigns` SET `status`='accepted' WHERE `assign_id`='%s'"%(ids)
		update(q)
		q1="UPDATE `cases` SET `status`='accepted' WHERE `case_id`='%s'"%(cid)
		update(q1)
		flash("Accepted Sucessfully!")
		return redirect(url_for('advocates.adv_view_client_assigncases'))

	if action == 'reject':
		q1="UPDATE `client_assigns` SET `status`='rejected' WHERE `assign_id`='%s'"%(ids)
		update(q1)
		flash("Rejected Sucessfully!")
		return redirect(url_for('advocates.adv_view_client_assigncases'))

	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS cli_name,`client_assigns`.`status`AS assign_status FROM `client_assigns` INNER JOIN `cli_registration` USING(client_id) INNER JOIN `cases` USING(`case_id`) WHERE `adv_id`='%s'"%(a_id)
	res=select(q)
	data['assigned_cases']=res
	return render_template('adv_view_client_assigncases.html',data=data)

@advocates.route('/adv_view_client_cases')
def adv_view_client_cases():
	data={}
	a_id=session['adv_id']

	if 'action' in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None

	if action == 'accept':
		q1="UPDATE `client_assigns` SET `status`='accepted' WHERE `case_id`='%s'"%(cid)
		update(q1)
		flash("Accepted Sucessfully!")
		return redirect(url_for('advocates.adv_view_client_cases'))

	if action == 'reject':
		q1="UPDATE `client_assigns` SET `status`='rejected' WHERE `case_id`='%s'"%(cid)
		update(q1)
		flash("Rejected Sucessfully!")
		return redirect(url_for('advocates.adv_view_client_cases'))

	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS cli_name,`client_assigns`.`status`AS assign_status FROM `client_assigns` INNER JOIN `cli_registration` USING(client_id) INNER JOIN `cases` USING(`case_id`) INNER JOIN `case_types` USING(`type_id`) WHERE `adv_id`='%s' "%(a_id)
	res=select(q)
	data['cli_cases']=res
	return render_template('adv_view_client_cases.html',data=data)

@advocates.route('/adv_view_clientdetails')
def adv_view_clientdetails():
	data={}

	ids=request.args['ids']

	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS clientname FROM `cases` INNER JOIN `cli_registration` USING(`client_id`) WHERE `case_id`='%s'"%(ids)
	res=select(q)
	data['cli_details']=res
	return render_template('adv_view_clientdetails.html',data=data)

@advocates.route('/adv_send_proposal',methods=['get','post'])
def adv_send_proposal():
	data={}
	a_id=session['adv_id']
	ids=request.args['ids']

	q="SELECT * FROM `proposals` INNER JOIN `cases` USING(`case_id`) WHERE `case_id`='%s'"%(ids)
	res=select(q)
	data['prop']=res

	if 'submit' in request.form:
		fee=request.form['fee']
		q="INSERT INTO `proposals`(`case_id`,`adv_id`,`fee`,`date_time`,`status`) VALUES('%s','%s','%s',now(),'%s')"%(ids,a_id,fee,'pending')
		insert(q)
		flash('proposal has been sent...')
		return redirect(url_for('advocates.adv_send_proposal',ids=ids))
	return render_template('adv_send_proposal.html',data=data)

@advocates.route('/adv_add_case_notes',methods=['get','post'])
def adv_add_case_notes():
	ids=request.args['ids']
	data={}
	q="SELECT *,`case_notes`.`description` AS c_desc FROM `case_notes` inner join cases using(case_id) WHERE `case_id`='%s'"%(ids)
	data['notes']=select(q)
	if 'submit' in request.form:
		note=request.form['note']
		q="INSERT INTO `case_notes`(`case_id`,`date_time`,`description`) VALUES('%s',NOW(),'%s')"%(ids,note)
		insert(q)
		flash('Case Note Added...')
		return redirect(url_for('advocates.adv_add_case_notes',ids=ids))
	return render_template('adv_add_case_notes.html',data=data)


@advocates.route('/adv_upload_case_files',methods=['get','post'])
def adv_upload_case_files():
	ids=request.args['ids']
	data={}
	q="SELECT * FROM `case_files` INNER JOIN cases USING(case_id) WHERE `case_id`='%s'"%(ids)
	data['upload']=select(q)
	if 'submit' in request.form:
		title=request.form['title']
		file=request.files['file']
		path="static/"+str(uuid.uuid4())+file.filename
		file.save(path)
		q="INSERT INTO `case_files`(`file_title`,`case_id`,`file_path`) VALUES('%s','%s','%s')"%(title,ids,path)
		insert(q)
		return redirect(url_for('advocates.adv_upload_case_files',ids=ids))

		flash('Success...')
	return render_template('adv_upload_case_files.html',data=data)





@advocates.route('/adv_view_rating')
def adv_view_rating():
	data={}
	advocate_id=session['adv_id']


	q="SELECT * FROM `ratings` WHERE `adv_id`='%s'"%(advocate_id)
	res=select(q)
	data['rating']=res

	return render_template('adv_view_rating.html',data=data)

@advocates.route('/advocate_chat_client',methods=['get','post'])
def advocate_chat_client():
	data={}

	advocate_id=session['adv_id']
	client_id=request.args['client_id']
	qry="SELECT CONCAT(first_name,' ',last_name) AS 'name' FROM `cli_registration` WHERE `client_id`='%s'"%(client_id)
	result=select(qry)
	data['names']='client name';

	if 'submit' in request.form:
		message=request.form['msg']

		# todo
		# add receiver id in args

		q2="INSERT INTO chats(sender_id,sender_type,receiver_id,receiver_type,message,`date_time`)VALUES('%s','advocate','%s','client','%s',NOW())"%(advocate_id,client_id,message)
		insert(q2)
		return redirect(url_for('advocates.advocate_chat_client',client_id=client_id))

	# todo
	# add receiver id in args

	q="SELECT * FROM chats WHERE (`sender_id`='%s' AND sender_type='client' AND `receiver_id`='%s') OR (`sender_id`='%s' AND `receiver_id`='%s' AND receiver_type='client')"%(client_id,advocate_id,advocate_id,client_id)
	res=select(q)
	data['msg']=res

	return render_template("advocate_chat_client.html",data=data)

