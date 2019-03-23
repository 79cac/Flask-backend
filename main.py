#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-09 
# @Author  : Wangyue 
# @Link    : http://example.org
# @Version : $1.0$

import sys
# import attackRelease.attackControl
import database.search
import database.store
from flask import Flask
from flask import request
from flask import session
from scapy.all import *
import os
from functools import wraps
import json
import threading
import time
import tempfile 

app = Flask(__name__)
app.secret_key = b'_6#y2L"F4Q8z\n\xec]/'
UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
		condition = {'attack_id': int(json.loads(request.get_data())['attackID'])}
		return json.dumps({'status':'OK','data':database.search.searchByAttackId(condition)})
	else:
		return json.dumps({'status':'log'})

@app.route('/searchByName', methods=['GET','POST'])
def searchByName():
	if 'username' in session:
		condition = {'attack_name': json.loads(request.get_data())['attackName']}
		return json.dumps({'status':'OK','data':database.search.searchByAttackId(condition)})
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
		condition = {'attack_id': json.loads(request.get_data())['attackID']}
		return json.dumps({'status':'OK','data':database.search.showDetails(condition)})
	else:
		return json.dumps({'status':'log'})

@app.route('/load', methods=['GET','POST'])
def load():
	if 'username' in session:
		if 'file' not in request.files:
			return json.dumps({'status':'file'})
		file = request.files['file']
		filename = file.filename
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		srcIP = request.form['srcIP']
		dstIP = request.form['dstIP']
		attack_name = request.form['attackName']
		plat_info = request.form['attackPlat']
		target_info = request.form['serverPlat']
		proto = request.form['proto']
		attack_info = [srcIP,dstIP,attack_name,plat_info,target_info,proto]
		rawPcap = rdpcap(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		if database.store.save_packet(rawPcap, attack_info):
			return json.dumps({'status':'OK'})
		else:
			return json.dumps({'status':'store'})
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
	