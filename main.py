#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-09 
# @Author  : Wangyue 
# @Link    : http://example.org
# @Version : $1.0$

import sys
import database.search
import database.store
import database.insert
import database.XMLGenerate
from flask import Flask
from flask import request
from flask import session
from scapy.all import *
import os
from functools import wraps
import json
from websocket import create_connection

app = Flask(__name__)
app.secret_key = b'_6#y2L"F4Q8z\n\xec]/'
UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/signIn', methods=['GET','POST'])
def signIn():
	if 'username' in session:
		return json.dumps({'status':'Already'})
	else:
		username = json.loads(request.get_data())['username']
		password = json.loads(request.get_data())['password']
		logTime = json.loads(request.get_data())['starttime']
		condition = {'username': username}
		result = database.search.verifyLog(condition)
		if len(result) != 0 and result[0][0] == password:
			database.insert.logInTime([username,logTime])
			session['username'] = username
			return json.dumps({'status':'OK'})
		else:
			return json.dumps({'status':'Wrong'})

@app.route('/logOut', methods=['GET','POST'])
def logOut():
	if 'username' in session:
		username = session['username']
		logTime = json.loads(request.get_data())['endtime']
		database.insert.logOutTime([username,logTime])
		session.pop('username', None)
		return json.dumps({'status':'OK'})
	else:
		return json.dumps({'status':'False'})

@app.route('/logInfo', methods=['GET','POST'])
def logInfo():
	if 'username' in session:
		condition = {'username': session['username']}
		result = database.search.logInfo(condition)
		return json.dumps({'status':'OK','data':result})
	else:
		return json.dumps({'status':'log'})

@app.route('/searchById', methods=['GET','POST'])
def searchById():
	if 'username' in session:
		condition = {'attack_id': json.loads(request.get_data())['attackID']}
		return json.dumps({'status':'OK','data':database.search.searchByAttackId(condition)})
	else:
		return json.dumps({'status':'log'})

@app.route('/searchByName', methods=['GET','POST'])
def searchByName():
	if 'username' in session:
		condition = {'attack_name': json.loads(request.get_data())['attackName']}
		return json.dumps({'status':'OK','data':database.search.searchByAttackName(condition)})
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
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'temp.pcap'))

		srcIP = request.form['srcIP']
		dstIP = request.form['dstIP']
		attack_name = request.form['attackName']
		plat_info = request.form['attackPlat']
		target_info = request.form['serverPlat']
		proto = request.form['proto']
		attack_info = [srcIP,dstIP,attack_name,plat_info,target_info,proto]
		rawPcap = rdpcap(os.path.join(app.config['UPLOAD_FOLDER'], 'temp.pcap'))
		if database.store.save_packet(rawPcap, attack_info):
			return json.dumps({'status':'OK'})
		else:
			return json.dumps({'status':'store'})
	else:
		return json.dumps({'status':'log'})

@app.route('/getFlowList', methods=['GET','POST'])
def getFlowList():
	if 'username' in session:
		return json.dumps({'status':'OK','data':database.search.getFlowList()})
	else:
		return json.dumps({'status':'log'})

@app.route('/getTaskList', methods=['GET','POST'])
def getTaskList():
	if 'username' in session:
		condition = {'username': session['username']} 
		return json.dumps({'status':'OK','data':database.search.getTaskList(condition)})
	else:
		return json.dumps({'status':'log'})

@app.route('/addTask', methods=['GET','POST'])
def addTask():
	if 'username' in session:
		username = session['username']
		task_name = json.loads(request.get_data())['taskName']
		attack_info = json.loads(request.get_data())['attackInfo']
		database.insert.addTask(username,task_name,attack_info)
		return json.dumps({'status':'OK'})
	else:
		return json.dumps({'status':'log'}) 

@app.route('/loadTask', methods=['GET','POST'])
def loadTask():
	if 'username' in session:
		username = session['username']
		task_name = json.loads(request.get_data())['taskName']
		condition = {'username': username, 'task_name': task_name}
		return json.dumps({'status':'OK','data':database.search.loadTask(condition)})
	else:
		return json.dumps({'status':'log'})

@app.route('/publish', methods=['GET','POST'])
def publish():
	if 'username' in session:
		username = session['username']
		attack_info = json.loads(request.get_data())['attackInfo']
		starttime = json.loads(request.get_data())['starttime']
		srcIP = json.loads(request.get_data())['srcIP']
		dstIP = json.loads(request.get_data())['dstIP']
		task_name = database.insert.publish(username,attack_info,starttime,srcIP,dstIP)
		#tell websocket server to release
		ws = create_connection("ws://192.168.233.150:1338")
		data = {'taskName':task_name, 'attackInfo':attack_info, 'srcIP':srcIP, 'dstIP':dstIP}
		ws.send('release:' + json.dumps(data))
		return json.dumps({'status':'OK'})
	else:
		return json.dumps({'status':'log'})

@app.route('/getReleaseInfo', methods=['GET','POST'])
def getReleaseInfo():
	if 'username' in session:
		condition = {'username': session['username']} 	
		result = database.search.getReleaseInfo(condition)	
		return json.dumps({'status':'OK','data':result})
	else:
		return json.dumps({'status':'log'})

@app.route('/finishRelease', methods=['GET','POST'])
def finishRelease():
	if 'username' in session:
		condition = {'username': session['username'],'task_name': json.loads(request.get_data())['taskName']}	
		result = database.insert.finishRelease(condition)	
		return json.dumps({'status':'OK'})
	else:
		return json.dumps({'status':'log'})

@app.route('/getDevicesInfo', methods=['GET','POST'])
def getDevicesInfo():
	if 'username' in session:
	    ws = create_connection("ws://192.168.233.150:1338")
	    ws.send('Ins:device')
	    result = ws.recv()
	    result = json.loads(result)
	    return json.dumps({'status':'OK','data':result})
	else:
	    return json.dumps({'status':'log'})

@app.route('/xml', methods=['GET','POST'])
def xml():
	if 'username' in session:
	    result = database.XMLGenerate.write2Xml(json.loads(request.get_data())['attackID'])
	    return json.dumps({'status':'OK','data':result})
	else:
	    return json.dumps({'status':'log'})

if __name__ == '__main__':
	app.run(debug=True,host='192.168.233.150',port=80)
	