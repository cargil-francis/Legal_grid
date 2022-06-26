from flask import *
from public import public
from admin import admin
from advocates import advocates
from client import client
app=Flask(__name__)
app.secret_key="admin"

app.register_blueprint(public)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(advocates,url_prefix='/advocates')
app.register_blueprint(client,url_prefix='/client')
app.run(debug=True, port=5008)

