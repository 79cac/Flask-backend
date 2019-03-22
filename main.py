#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-09 
# @Author  : Wangyue 
# @Link    : http://example.org
# @Version : $1.0$

import sys
# import attackRelease.attackControl
import database.search
from flask import Flask
from flask import request
from flask import session
from functools import wraps
import json
import threading
import time

app = Flask(__name__)
app.secret_key = b'_6#y2L"F4Q8z\n\xec]/'

@app.route('/signIn', methods=['GET','POST'])
def signIn():
	if 'username' in session:
		return json.dumps({'status':'Already'})
	else:
		session['username'] = json.loads(request.get_data())['username']
		return json.dumps({'status':'OK'})

@app.route('/logOut', methods=['GET','POST'])
def logOut():
	if 'username' in session:
		session.pop('username', None)
		return json.dumps({'status':'OK'})
	else:
		return json.dumps({'status':'False'})

@app.route('/searchById', methods=['GET','POST'])
def searchById():
	if 'username' in session:
		return json.dumps({'status':'OK','data':database.search.searchByAttackId(json.loads(request.get_data())['attackID'])})
	else:
		return json.dumps({'status':'log'})
		
@app.route('/listAll', methods=['GET','POST'])
def listAll():
	if 'username' in session:		
		return json.dumps({'status':'OK','data':database.search.listAll()})
	else:
		return json.dumps({'status':'log'})

@app.route('/showDetails',methods=['GET','POST'])
def showDetails():
	if 'username' in session:
		return json.dumps({'status':'OK','data':database.search.showDetails(json.loads(request.get_data())['attackID'])})
	else:
		return json.dumps({'status':'log'})
# @app.route('/release',methods=['GET','POST'])
# def release():
# 	data = json.loads(request.get_data())
# 	F = attackRelease.attackControl.attackInitial(data['attackID'],data['hackerIP'],data['serverIP'],data['useTimeStamp'],data['isAttacker'])
# 	F.run()
# 	return 'Released Successfully'

@app.route('/checkAlive',methods=['GET','POST'])
def checkAlive():
	return '1'

if __name__ == '__main__':
	app.run(debug=True,host='192.168.233.150',port=80)
	