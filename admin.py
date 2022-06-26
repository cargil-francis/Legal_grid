from flask import*
from database import*
admin=Blueprint('admin',__name__)

@admin.route('/admin_home')
def admin_home():
	return render_template('admin_home.html')

@admin.route('/admin_view_advocates')
def admin_view_advocates():
	data={}

	if 'action' in request.args:
		action=request.args['action']
		ids=request.args['ids']
	else:
		action=None

	if action == 'accept':
		q="UPDATE `login` SET `user_type`='advocate' WHERE `login_id`='%s'"%(ids)
		update(q)
		q1="UPDATE `adv_registration` SET `status`='accepted' WHERE `login_id`='%s'"%(ids)
		update(q1)
		flash("Accepted Sucessfully!")
		return redirect(url_for('admin.admin_view_advocates'))

	if action == 'reject':
		q="UPDATE `login` SET `user_type`='rejected' WHERE `login_id`='%s'"%(ids)
		update(q)
		q1="UPDATE `adv_registration` SET `status`='rejected' WHERE `login_id`='%s'"%(ids)
		update(q1)
		flash("Rejected Sucessfully!")
		return redirect(url_for('admin.admin_view_advocates'))

	q="SELECT * FROM adv_registration INNER JOIN `login` USING(`login_id`)"
	res=select(q)
	data['advocates']=res

	return render_template('admin_view_advocates.html',data=data)

@admin.route('/admin_manage_casetype',methods=['get','post'])
def admin_manage_casetype():
	data={}

	if 'action' in request.args:
		action=request.args['action']
		ids=request.args['ids']
	else:
		action=None

	if action=='delete':
		q="DELETE FROM `case_types` WHERE `type_id`='%s'"%(ids)
		delete(q)
		flash("Deleted Sucessfully!")
		return redirect(url_for('admin.admin_manage_casetype'))

	if action=='update':
		q="SELECT * FROM case_types WHERE type_id='%s'"%(ids)
		res=select(q)
		data['upd_case']=res


	if 'submits' in request.form:
		type_name=request.form['type_name']
		descrip=request.form['description']

		q="UPDATE `case_types` SET `type_name`='%s',`description`='%s' WHERE `type_id`='%s'"%(type_name,descrip,ids)
		update(q)
		return redirect(url_for('admin.admin_manage_casetype'))



	if 'submit' in request.form:
		type_name=request.form['type_name']
		descrip=request.form['description']
		q="INSERT INTO case_types(type_name,description)VALUES('%s','%s')"%(type_name,descrip)
		insert(q)
		return redirect(url_for('admin.admin_manage_casetype'))
	q="SELECT * FROM case_types "
	res=select(q)
	data['advocates']=res	
	
	return render_template('admin_manage_casetype.html',data=data)

@admin.route('/admin_manage_lawdetails',methods=['get','post'])
def admin_manage_lawdetails():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		ids=request.args['ids']
	else:
	 	action=None

	if action=='delete':
		q="DELETE FROM `law_details` WHERE `law_id`='%s'"%(ids)
		delete(q)
		flash("Deleted Sucessfully!")
		return redirect(url_for('admin.admin_manage_lawdetails'))

	if action=='update':
		q="SELECT * FROM law_details WHERE law_id='%s'"%(ids)
		res=select(q)
		data['upd_law']=res

	if 'submits' in request.form:
		title=request.form['title']
		ipccode=request.form['ipc_code']
		descrip=request.form['description']
		penalty=request.form['penalty']

		q="UPDATE `law_details` SET `title`='%s',`ipc_code`='%s',`description`='%s',`penalty`='%s' WHERE `law_id`='%s'"%(title,ipccode,descrip,penalty,ids)
		update(q)
		return redirect(url_for('admin.admin_manage_lawdetails'))

	if 'submit' in request.form:
		title=request.form['title']
		ipccode=request.form['ipc_code']
		descrip=request.form['description']
		penalty=request.form['penalty']

		q="INSERT INTO law_details(title,ipc_code,description,penalty)VALUES('%s','%s','%s','%s')"%(title,ipccode,descrip,penalty)
		insert(q)
		return redirect(url_for('admin.admin_manage_lawdetails'))
	q="SELECT * FROM law_details "
	res=select(q)
	data['advocates']=res	
	return render_template('admin_manage_lawdetails.html',data=data)

@admin.route('/view_users')
def view_users():
	data={}

	q="SELECT * FROM cli_registration"
	res=select(q)
	data['advocates']=res
	return render_template('view_users.html',data=data)

@admin.route('/view_complaints_sendreply',methods=['get','post'])
def view_complaints_sendreply():
	data={}



	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS cli_name FROM complaints INNER JOIN `cli_registration` USING(`client_id`)"
	res=select(q)
	data['msgs']=res

	i=1
	for row in data['msgs']:
		if 'submit'+str(i) in request.form:
			reply=request.form['reply'+str(i)]
			q="UPDATE complaints SET reply='%s',date_time=NOW() WHERE `complaint-id`='%s'"%(reply,row['complaint-id'])
			update(q)
			flash("Replied")
			return redirect(url_for("admin.view_complaints_sendreply"))
		i=i+1
	return render_template('view_complaints_sendreply.html',data=data)

@admin.route('/admin_view_cases')
def admin_view_cases():
	data={}

	ids=request.args['ids']

	q="SELECT *,CONCAT(`adv_registration`.`first_name`,' ',`adv_registration`.`last_name`) AS adv_name FROM `cases` INNER JOIN `cli_registration` USING(`client_id`) INNER JOIN `case_types` USING(`type_id`) INNER JOIN `client_assigns` USING(`case_id`) INNER JOIN `adv_registration` USING(`adv_id`) WHERE (`client_assigns`.`client_id`='%s')"%(ids)
	res=select(q)
	data['cases']=res
	return render_template('admin_view_cases.html',data=data)
